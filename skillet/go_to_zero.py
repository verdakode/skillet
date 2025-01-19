"""Script to move all joints back to their configured zero positions."""

import logging
import time
import traceback
import pykos
from skillet.setup.maps import ACTUATOR_NAME_TO_ID

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Move all actuators back to their configured zero positions."""
    kos = pykos.KOS(ip="10.33.11.238")

    # Create commands list in correct format
    commands = []
    for actuator_id in ACTUATOR_NAME_TO_ID.values():
        command = {"actuator_id": actuator_id, "position": 0.0, "velocity": 0.0, "torque": 0.0}  # Optional  # Optional
        commands.append(command)

    try:
        # Get initial states
        for name, act_id in ACTUATOR_NAME_TO_ID.items():
            state = kos.actuator.get_actuators_state([act_id])
            logger.info(f"Initial state for {name}: {state}")

        # Send commands
        logger.info("Moving all actuators to zero")
        kos.actuator.command_actuators(commands)

        time.sleep(1.0)  # Wait for movement

        # Verify final states
        for name, act_id in ACTUATOR_NAME_TO_ID.items():
            state = kos.actuator.get_actuators_state([act_id])
            logger.info(f"Final state for {name}: {state}")

    except Exception as e:
        logger.error(f"Error commanding actuators: {str(e)}")
        logger.error(f"Traceback:\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()
