"""Script to move joints to zero position.
Make sure you have configured and zeroed the joints before running this script.
Uses wlan0 (10.33.11.238) for robot control.
"""

# Standard library imports
import logging
import time
import traceback

# Third-party imports
try:
    import colorlogging
    import pykos
except ImportError:
    logging.warning("colorlogging module not found. Colored output won't be available.")

# Local imports
from skillet.examples.move_joint_a_little import move_joint_a_little
from skillet.setup.maps import ACTUATOR_NAME_TO_ID

# Constants
MOVE_DEGREES = -5.0  # Moving in negative direction towards zero
ROBOT_IP = "10.33.11.238"  # wlan0 interface IP

logger = logging.getLogger(__name__)


def main() -> None:
    """Move all joints towards zero position with error handling."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    if "colorlogging" in globals():
        colorlogging.configure()

    logger.info("Starting joint movement sequence using %s", ROBOT_IP)

    failed_joints = []

    # Move each joint multiple times to ensure reaching zero
    for iteration in range(8):  # Multiple small movements
        logger.info(f"Starting iteration {iteration + 1}/8")
        for joint_name in ACTUATOR_NAME_TO_ID:
            try:
                logger.info("Moving joint towards zero: %s", joint_name)
                move_joint_a_little(joint_name, MOVE_DEGREES)
                logger.info("Successfully moved joint: %s", joint_name)
                time.sleep(1.0)  # Delay for stability
            except Exception as e:
                logger.error("Failed to move joint %s: %s", joint_name, str(e))
                logger.error("Traceback:\n%s", traceback.format_exc())
                if joint_name not in failed_joints:  # Only add unique failures
                    failed_joints.append(joint_name)
                logger.info("Continuing with next joint...")

        # Add a longer pause between complete cycles
        time.sleep(2.0)

    # Log summary
    if failed_joints:
        logger.error("=== Failed Joints ===")
        logger.error("Failed to move %d joints: %s", len(failed_joints), ", ".join(failed_joints))
    else:
        logger.info("All joints successfully moved")


if __name__ == "__main__":
    main()
