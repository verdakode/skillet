"""Script to enable or disable torque for actuators."""

import logging
import argparse
import pykos
from skillet.setup.maps import ACTUATOR_NAME_TO_ID

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def set_torque(enable: bool) -> None:
    """Enable or disable torque for all actuators.
    
    Args:
        enable: True to enable torque, False to disable
    """
    kos = pykos.KOS(ip="192.168.42.1")
    action = "Enabling" if enable else "Disabling"
    logger.info(f"{action} torque for all actuators")
    
    for name, actuator_id in ACTUATOR_NAME_TO_ID.items():
        try:
            kos.actuator.configure_actuator(actuator_id=actuator_id, torque_enabled=enable)
            state = kos.actuator.get_actuators_state([actuator_id])
            logger.info(f"Actuator {name}: {state}")
        except Exception as e:
            logger.error(f"Error configuring actuator {name}: {str(e)}")


def main() -> None:
    """Parse arguments and set torque state."""
    parser = argparse.ArgumentParser(description="Enable or disable torque for all actuators")
    parser.add_argument("--enable", action="store_true", help="Enable torque")
    parser.add_argument("--disable", action="store_true", help="Disable torque")
    
    args = parser.parse_args()
    
    if args.enable and args.disable:
        logger.error("Cannot both enable and disable torque")
        return
    
    if not args.enable and not args.disable:
        logger.error("Must specify either --enable or --disable")
        return
        
    set_torque(args.enable)


if __name__ == "__main__":
    main() 