import sys
import time
import subprocess

from typing import Tuple

try:
    import pyautogui #type: ignore
except ImportError as error:
    print("Please Install PyAutoGui correctly!")
    sys.exit()

try:
    from pyvda import VirtualDesktop, get_virtual_desktops
except ImportError as _:
    print("Please Install PyVDA correctly!")
    sys.exit()

# ----------------------------------------------------------------------------

def check_dependencies() -> Tuple[bool, str]:
    """
    Checks the dependencies and alerts if there are some broken
    and some actions needs to be taken
    """
    try:
        subprocess.check_output(["py", "-m", "pip", "check"], universal_newlines=True)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.output

# ----------------------------------------------------------------------------

def print_dependencies_check(data_string: str) -> str:
    """
    Prints the results of the dependencies check
    """
    try:
        from colorama import Fore, Style, init
        init()
        start_ok_color = Fore.GREEN
        start_fault_color = Fore.RED
        stop_color = Style.RESET_ALL
    except ImportError as _:
        start_ok_color = start_fault_color = stop_color = ""
    if data_string is None:
        return f"{start_ok_color}OK{stop_color}"
    return f"{start_fault_color}{data_string}{stop_color}"

# ----------------------------------------------------------------------------

def click_on_screen(image_path: str) -> None:
    """
    Responsible for clicking at the right position on the screen 
    """
    button = pyautogui.locateOnScreen(image_path)
    button_center = pyautogui.center(button)
    pyautogui.click(button_center)

# ----------------------------------------------------------------------------

def main() -> None:

    # Global constants
    NUM_DESKTOPS: int = 4

    NO_BROKEN_DEPENDENCIES, DEPENDENCIES_CHECK_RESULT = check_dependencies()
    if not NO_BROKEN_DEPENDENCIES:
        print(f"Some dependencies appear to be broken!\n")
        print(f"{'==' * 64}")
        print(print_dependencies_check(DEPENDENCIES_CHECK_RESULT))
        print(f"{'==' * 64}")

    INTERPRETER = sys.executable
    print(f"The interpreter being used is {INTERPRETER}")

    # get the number of active desktops (should be 4 for my machine)
    num_active_desktops = len(get_virtual_desktops())
    assert (num_active_desktops == NUM_DESKTOPS)

    # open the applications on desktop 1
    VirtualDesktop(1).go()
    click_on_screen("./templates/chrome.png")

    time.sleep(1)

    # open the applications on desktop 2
    VirtualDesktop(2).go()
    click_on_screen("./templates/outlook.png")
    click_on_screen("./templates/terminal.png")
    click_on_screen("./templates/vscode.png")

    time.sleep(2) # give some time for the IDE windows to load properly

    click_on_screen("./templates/vstool.png")
    click_on_screen("./templates/adobe.png")
    click_on_screen("./templates/onenote.png")
    click_on_screen("./templates/pycharm.png")
    click_on_screen("./templates/notes.png")
    click_on_screen("./templates/whiteboard.png")

    # indicate that the program is complete
    pyautogui.alert(text='Execution Finished!', title='Finished', button='OK')

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------
