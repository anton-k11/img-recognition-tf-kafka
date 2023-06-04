# Matplotlib Processing Times 
The scripts currently parse the output of `docker compose logs decision-consumer` and plots the collected data.
It assumes the logs are in the following format:

```
2023-05-30 10:57:26,055 - INFO - Delivered in 201 ms.
2023-05-30 10:57:26,602 - INFO - Payload: {'label': 'Granny Smith', 'probability': 66.0491, 'elapsed': 117} - Headers: {'timestamp': b'1685444246377', 'producer_id': b'911294b90037'}
```

For instructions how to run the scripts refer to [Main project README](../README.md#plot-delivery-times)