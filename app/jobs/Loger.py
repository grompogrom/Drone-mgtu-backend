from cflib.crazyflie.log import LogConfig, Log

from app.jobs.config.scaning import SENSOR_READING_INTERVAL


class Logger:

    def __init__(self, loger: Log):
        self.logger = loger
        self.pos_config = self._create_pos_config()
        self.measurment_config = self._create_measurement_config()
        self.power_config = self._create_power_managment_config()
        self.logger.add_config(self.pos_config)     # TODO move to start_logging
        self.logger.add_config(self.measurment_config)      # TODO move to start_logging
        self.logger.add_config(self.power_config)

    def start_logging(self):
        self.pos_config.start()
        self.measurment_config.start()
        self.power_config.start()

    def stop_loging(self):
        self.pos_config.stop()
        self.measurment_config.stop()
        self.power_config.stop()

    def add_pos_listener(self, listener):
        self.pos_config.data_received_cb.add_callback(listener)

    def add_measurement_listener(self, listener):
        self.measurment_config.data_received_cb.add_callback(listener)

    def add_power_listener(self, listener):
        self.power_config.data_received_cb.add_callback(listener)

    def _create_pos_config(self):
        print("pos config created")
        lpos = LogConfig(name='Position', period_in_ms=SENSOR_READING_INTERVAL)
        lpos.add_variable('stateEstimate.x')
        lpos.add_variable('stateEstimate.y')
        lpos.add_variable('stateEstimate.z')
        return lpos

    def _create_power_managment_config(self):
        lpm = LogConfig(name='Power', period_in_ms=1000)
        lpm.add_variable('pm.batteryLevel')
        lpm.add_variable('pm.vbat')
        lpm.add_variable('pm.chargeCurrent')
        return lpm

    def _create_measurement_config(self):
        lmeas = LogConfig(name='Meas', period_in_ms=SENSOR_READING_INTERVAL)
        lmeas.add_variable('range.front')
        lmeas.add_variable('range.back')
        lmeas.add_variable('range.up')
        lmeas.add_variable('range.left')
        lmeas.add_variable('range.right')
        lmeas.add_variable('range.zrange')
        lmeas.add_variable('stabilizer.roll')
        lmeas.add_variable('stabilizer.pitch')
        lmeas.add_variable('stabilizer.yaw')
        return lmeas
