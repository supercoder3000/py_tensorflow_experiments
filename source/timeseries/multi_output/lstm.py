import tensorflow as tf

from data_types.training_result import TrainingResult
from data_types.training_set import TrainingSet
from timeseries.build import compile_and_fit
from timeseries.window_generator import WindowGenerator


def evaluate_lstm_multi_output(
        training_set: TrainingSet
) -> TrainingResult:
    wide_window = WindowGenerator(
        input_width=24,
        label_width=24,
        shift=1,
        training_set=training_set
    )

    lstm_model = tf.keras.models.Sequential([
        # Shape [batch, time, features] => [batch, time, lstm_units]
        tf.keras.layers.LSTM(32, return_sequences=True),
        # Shape => [batch, time, features]
        tf.keras.layers.Dense(units=training_set.num_features)
    ])

    compile_and_fit(lstm_model, wide_window)

    metric_index = lstm_model.metrics_names.index('mean_absolute_error')

    return TrainingResult(
        validation_performance=lstm_model.evaluate(wide_window.val)[metric_index],
        performance=lstm_model.evaluate(wide_window.test, verbose=0)[metric_index]
    )