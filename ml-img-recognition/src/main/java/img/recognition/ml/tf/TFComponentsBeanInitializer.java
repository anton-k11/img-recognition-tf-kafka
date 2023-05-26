package img.recognition.ml.tf;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;
import org.tensorflow.Graph;
import org.tensorflow.proto.framework.GraphDef;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Component
public class TFComponentsBeanInitializer {

    @Bean
    public Graph tfModelGraph(@Value("${tf.frozenModelPath}") String tfFrozenModelPath) throws IOException {
        Resource graphResource = getResource(tfFrozenModelPath);

        Graph graph = new Graph();
        GraphDef graphDef = GraphDef.parseFrom(graphResource.getInputStream());
        graph.importGraphDef(graphDef);
        log.info("Loaded Tensorflow model");
        return graph;
    }

    private Resource getResource(@Value("${tf.frozenModelPath}") String tfFrozenModelPath) {
        Resource graphResource = new FileSystemResource(tfFrozenModelPath);
        if(!graphResource.exists()) {
            graphResource = new ClassPathResource(tfFrozenModelPath);
        }
        if(!graphResource.exists()) {
            throw new IllegalArgumentException(String.format("File %s does not exist", tfFrozenModelPath));
        }
        return graphResource;
    }

    @Bean
    public List<String> tfModelLabels(@Value("${tf.labelsPath}") String labelsPath) throws IOException {
        Resource labelsRes = getResource(labelsPath);
        log.info("Loaded model labels");
        return IOUtils.readLines(labelsRes.getInputStream(), StandardCharsets.UTF_8).stream()
                .map(label -> label.substring(label.contains(":") ? label.indexOf(":")+1 : 0)).collect(Collectors.toList());
    }
}
