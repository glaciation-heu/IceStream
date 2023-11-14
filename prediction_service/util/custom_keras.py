import tensorflow as tf


class CustomSaveCheckpoint(tf.keras.callbacks.Callback):
    def __init__(self, forecaster):
        self.forecaster = forecaster
    

    def on_epoch_end(self, epoch, logs=None):
        # Logs is dict
        if logs['val_loss'] < self.forecaster.best_val_loss:
            print(f'\nNew best val loss: {logs["val_loss"]}')
            self.forecaster.best_val_loss = logs['val_loss']
            self.forecaster.model = self.forecaster.current
            self.forecaster.save_model()
            

