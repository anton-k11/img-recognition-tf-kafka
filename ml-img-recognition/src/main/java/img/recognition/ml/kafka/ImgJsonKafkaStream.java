package img.recognition.ml.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import img.recognition.ml.tf.ClassifyImageService;
import img.recognition.ml.tf.ClassifyImageService.LabelWithProbability;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Slf4j
@Service
@RequiredArgsConstructor(onConstructor_={@Autowired})
public class ImgJsonKafkaStream {

    private final ClassifyImageService classifyImageService;
    private final KafkaStreamConfig config;
    private final ObjectMapper mapper = new ObjectMapper();

    @Autowired
    public void kafkaStreams(StreamsBuilder streamsBuilder) {
        String consumerTopic = config.getConsumerTopic();
        String producerTopic = config.getProducerTopic();
        log.info("Consuming from {} and producing to {} topics", consumerTopic, producerTopic);

        KStream<String, byte[]> stream = streamsBuilder
                .stream(consumerTopic, Consumed.with(Serdes.String(), Serdes.ByteArray()));

        // Transform the image into JSON (replace with your own transformation code)
        KStream<String, String> transformedStream = stream.mapValues(
                value -> {
                    log.info("Message with length {} consumed", value.length);
                    // Replace this with your transformation logic
                    String json = null;
                    try {
                        json = transformImageToJson(value);
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }

                    // Return the new key-value pair with preserved headers
                    return json;
                });

        transformedStream.to(producerTopic);

        // Print the transformed stream (optional)
        //transformedStream.print(Printed.toSysOut());
    }

    // Replace this with your own image-to-JSON transformation logic
    private String transformImageToJson(byte[] image) throws JsonProcessingException {
        LabelWithProbability labelWithProbability = classifyImageService.classifyImage(image);

        String json = mapper.writeValueAsString(labelWithProbability);
        log.info("Classified {}", json);
        return json;
    }


}
