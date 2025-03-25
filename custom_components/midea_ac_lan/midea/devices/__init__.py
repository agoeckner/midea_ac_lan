from homeassistant.core import HomeAssistant
from homeassistant.helpers.importlib import async_import_module


async def device_selector(
    hass: HomeAssistant,
    name: str,
    device_id: int,
    device_type: int,
    ip_address: str,
    port: int,
    token: str,
    key: str,
    protocol: int,
    model: str,
    subtype: int,
    customize: str
):
    try:

        if device_type < 0xA0:
            device_path = f"{__package__}.{'x%02x' % device_type}.device"
        else:
            device_path = f"{__package__}.{'%02x' % device_type}.device"
        module = await async_import_module(hass, device_path)
        device = module.MideaAppliance(
            name=name,
            device_id=device_id,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            protocol=protocol,
            model=model,
            subtype=subtype,
            customize=customize
        )
    except ModuleNotFoundError:
        device = None
    return device
