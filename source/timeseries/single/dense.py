import tensorflow as tf

from data_types.training_result import TrainingResult
from data_types.training_set import TrainingSet
from timeseries.build import compile_and_fit
from timeseries.window_generator import WindowGenerator


def evaluate_dense(
        training_set: TrainingSet
) -> TrainingResult:
    dense = tf.keras.Sequential([
        tf.keras.layers.Dense(units=64, activation='relu'),
        tf.keras.layers.Dense(units=64, activation='relu'),
        tf.keras.layers.Dense(units=1)
    ])

    single_step_window = WindowGenerator(
        input_width=1,
        label_width=1,
        shift=1,
        training_set=training_set,
        label_columns=['T (degC)']
    )

    compile_and_fit(dense, single_step_window)

    metric_index = dense.metrics_names.index('mean_absolute_error')

    return TrainingResult(
        validation_performance=dense.evaluate(single_step_window.val)[metric_index],
        performance=dense.evaluate(single_step_window.test, verbose=0)[metric_index]
    )