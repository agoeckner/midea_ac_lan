from homeassistant.components.humidifier import *
from homeassistant.components.humidifier.const import *
from homeassistant.const import (
    TEMP_CELSIUS,
    PRECISION_WHOLE,
    PRECISION_HALVES,
    ATTR_TEMPERATURE,
    CONF_DEVICE_ID,
    STATE_ON,
    STATE_OFF
)
from .const import (
    DOMAIN,
    DEVICES,
)
from .midea_devices import MIDEA_DEVICES
from .midea_entity import MideaEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    device_id = config_entry.data.get(CONF_DEVICE_ID)
    device = hass.data[DOMAIN][DEVICES].get(device_id)
    humidifiers = []
    for entity_key, config in MIDEA_DEVICES[device.device_type]["entities"].items():
        if config["type"] == "humidifier":
            if device.device_type == 0xa1:
                humidifiers.append(MideaA1Humidifier(device, entity_key))
            if device.device_type == 0xfd:
                humidifiers.append(MideaFDHumidifier(device, entity_key))
    async_add_entities(humidifiers)


class MideaHumidifier(MideaEntity, HumidifierEntity):
    def __init__(self, device, entity_key):
        super().__init__(device, entity_key)

    @property
    def target_humidity(self):
        return self._device.get_attribute("target_humidity")

    @property
    def mode(self):
        return self._device.get_attribute("mode")

    @property
    def available_modes(self):
        return self._device.modes

    def set_humidity(self, humidity: int):
        self._device.set_attribute("target_humidity", humidity)

    def set_mode(self, mode: str):
        self._device.set_attribute("mode", mode)

    @property
    def min_humidity(self):
        return self._min_humidity

    @property
    def max_humidity(self):
        return self._max_humidity

    @property
    def state(self):
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def is_on(self):
        return self._device.get_attribute(attr="power")

    def turn_on(self):
        self._device.set_attribute(attr="power", value=True)

    def turn_off(self):
        self._device.set_attribute(attr="power", value=False)

    def update_state(self, status):
        try:
            self.schedule_update_ha_state()
        except Exception:
            pass


class MideaA1Humidifier(MideaHumidifier):
    def __init__(self, device, entity_key):
        super().__init__(device, entity_key)
        self._min_humidity = 35
        self._max_humidity = 85

    @property
    def device_class(self):
        return HumidifierDeviceClass.DEHUMIDIFIER

    @property
    def supported_features(self):
        return HumidifierEntityFeature.MODES


class MideaFDHumidifier(MideaHumidifier):
    def __init__(self, device, entity_key):
        super().__init__(device, entity_key)
        self._min_humidity = 35
        self._max_humidity = 85

    @property
    def device_class(self):
        return HumidifierDeviceClass.HUMIDIFIER

    @property
    def supported_features(self):
        return HumidifierEntityFeature.MODES
