"""
Primary window: "MayaWindow"

# Full path of panel + control + window
p = cmds.panel(panelname, q, control)

# Layout preset to determine button layout
cmds.paneLayout(controlname, q, configuration, activePane, activePaneIndex, parent)

# Similar to paneLayout
cmds.layout(layoutname, q, configuration)

# Window props
widthHeight [x, y]
topleftcorner [y down, x right]
"""

import sys
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

sys.stdout = sys.__stdout__

windowID = 'PlayView'
helpID = 'PlayViewHelp'
custom_viewport = ""  # Saves panel name for future playback
custom_viewport_tmp = ""  # Temp variable


def play_button(*args):
    return mel.eval(
        "undoInfo -stateWithoutFlush off;"
        "playButtonForward;"
        "undoInfo -stateWithoutFlush on;"
    )


def play_view(make_default, view, *args):
    """Play with specific viewport."""
    sys.stdout.writelines(["{}\n".format(view)])
    if cmds.checkBox(make_default, q=True, value=True):
        custom_viewport = view
    else:
        custom_viewport = ""
    cmds.setFocus(view)
    destroy_window()
    play_button()


def gui(ctrl, pWindowTitle, winID, TLC, *args):
    """Draw the main window."""
    win_draw = cmds.window(
        winID,
        title=pWindowTitle,
        titleBar=False,
        sizeable=False,
        resizeToFitChildren=True,
        tlc=TLC,
        wh=(250, 150)
    )
    rowcol = cmds.rowColumnLayout(
        numberOfColumns=1,
        columnWidth=[(1, 245)],
        columnOffset=[(1, 'both', 5)]
    )
    cmds.separator(h=5, style='none')
    cmds.text(label='Select a viewport to play from.')
    cmds.separator(h=5, style='none')
    cmds.rowLayout(
        parent=rowcol,
        numberOfColumns=3,
        columnAttach=[
            (1, 'both', 0),
            (2, 'both', 5),
            (3, 'both', 0)
        ],
        columnWidth=[
            (1, 75),  # Total == 250 - margins
            (2, 90),
            (3, 75)
        ]
    )
    cmds.button(label='Help', command=help_call)
    makeDefault = cmds.checkBox(label='Make Default')
    cmds.button(label='Cancel', command=destroy_window)

    cmds.separator(parent=rowcol, h=1, style='none')

    lconfig = get_layout_config(ctrl)
    lconfigarray = get_layout_child_array(ctrl)
    sys.stdout.writelines(["Format: {}\n".format(lconfig), "Children: {}\n".format(lconfigarray)])
    button_grid(rowcol, lconfigarray, lconfig, makeDefault)

    cmds.showWindow()

    cmds.window(
        win_draw, e=True, tlc=TLC
    )


def button_grid(parent, child_array, layout_config=None, default=False, *args):
    """Make a UI grid layout based on result from get_layout_config()."""

    if layout_config == "single":
        # 3*3, center button
        RC = cmds.columnLayout(p=parent)
        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "quad":
        # 4*4
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "horizontal2":
        # 3*4, center 2 buttons
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "vertical2":
        # 4*3, center 2 buttons
        RC = cmds.rowColumnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "horizontal3":
        # 3*5, center 3 buttons
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)

        return RC
    elif layout_config == "vertical3":
        # 5*3, center 3 buttons
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "top3":
        # 4*4, top 2, buttom 1
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=child_array[2])
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "left3":
        # 4*4
        RC = cmds.columnLayout(p=parent)
        row1 = cmds.rowLayout(nc=4)

        col1 = cmds.columnLayout(p=row1, cw=5)
        cmds.separator(p=col1, style='none')

        col2 = cmds.columnLayout(p=row1)
        cmds.separator(p=col2, h=5, style='none')
        cmds.button(p=col2, label="", command=partial(play_view, default, child_array[0]))
        cmds.button(p=col2, label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(p=col2, h=5, style='none')

        col3 = cmds.columnLayout(p=row1)
        cmds.separator(p=col3, h=5, style='none')
        cmds.button(p=col3, label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(p=col3, h=5, style='none')

        col4 = cmds.columnLayout(p=row1, cw=5)
        cmds.separator(p=col4, style='none')

        return RC
    elif layout_config == "bottom3":
        # 4*4
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
        pass
    elif layout_config == "right3":
        # 4*4
        RC = cmds.columnLayout(p=parent)
        row1 = cmds.rowLayout(nc=4)

        col1 = cmds.columnLayout(p=row1, cw=5)
        cmds.separator(p=col1, style='none')

        col2 = cmds.columnLayout(p=row1)
        cmds.separator(p=col2, h=5, style='none')
        cmds.button(p=col2, label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(p=col2, h=5, style='none')

        col3 = cmds.columnLayout(p=row1)
        cmds.separator(p=col3, h=5, style='none')
        cmds.button(p=col3, label="", command=partial(play_view, default, child_array[1]))
        cmds.button(p=col3, label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(p=col3, h=5, style='none')

        col4 = cmds.columnLayout(p=row1, cw=5)
        cmds.separator(p=col4, style='none')

        return RC
    elif layout_config == "horizontal4":
        # 3*6
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "vertical4":
        # 6*3
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=6)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "top4":
        # 5*4
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "left4":
        # 4*5
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=4)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "bottom4":
        # 5*4
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=3)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=5)
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC
    elif layout_config == "right4":
        # 4*5
        RC = cmds.columnLayout(p=parent)

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=5)
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[1]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=5)
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[0]))
        cmds.button(label="", command=partial(play_view, default, child_array[2]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=5)
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.separator(h=5, style='none')
        cmds.button(label="", command=partial(play_view, default, child_array[3]))
        cmds.separator(h=5, style='none')

        cmds.rowLayout(parent=RC, nc=1)
        cmds.separator(h=5, style='none')

        return RC


def help_call(*args):
    """Open a text window with help information."""
    helpText = (
        'PlayView: Always play a specific viewport.\n'
        'by Jeffrey "italic" Hoover'
    )

    if cmds.window(helpID, exists=True):
        cmds.deleteUI(helpID)

    cmds.window(helpID,
                title='PlayViewHelp',
                widthHeight=[300, 200],
                sizeable=True,
                resizeToFitChildren=True)
    cmds.columnLayout(width=300)
    cmds.scrollField(wordWrap=True,
                     text=helpText,
                     editable=False,
                     width=300,
                     height=200,
                     font='smallPlainLabelFont')

    cmds.showWindow()


def draw_PlayView(pWindowTitle, *args):
    wInd = 0
    WH = [-125, -75]  # Window dimensions are 250*150, negated for addition
    for panel in cmds.getPanel(vis=True):
        for w in get_windows():
            if cmds.panel(panel, q=True, control=True).startswith(w):
                WC = get_window_center(w)
                WH.reverse()
                TLC = [sum(x) for x in zip(WC, WH)]

                sys.stdout.writelines(["\n{}\n".format(w), "TLC: {}\n".format(TLC), "WC: {}\n".format(WC)])

                ctrl = cmds.panel(panel, q=True, control=True)
                gui(ctrl, pWindowTitle, "{}{}".format(windowID, wInd), TLC)
                wInd += 1


def get_windows(*args):
    """Get all available windows."""
    return cmds.lsUI(windows=True)


def get_window_center(window, *args):
    """Get window's center position."""
    WH = [l // 2 for l in cmds.window(window, q=True, wh=True)]
    WH.reverse()
    TLC = cmds.window(window, q=True, tlc=True)
    return [sum(x) for x in zip(TLC, WH)]


def get_layout(window, *args):
    """Get layout of given window."""
    for widget in sorted(cmds.lsUI(long=True, controlLayouts=True)):
        if widget.startswith(window):
            yield widget


def get_layout_control(ctrl, *args):
    """Get layout's control."""
    return "|".join(ctrl.split("|")[:-1])


def get_layout_config(ctrl, *args):
    """Get layout's configuration."""
    control = get_layout_control(ctrl)
    ctrllayout = cmds.paneLayout(control, q=True, configuration=True)
    return ctrllayout


def get_layout_child_array(ctrl, *args):
    """Get layout's child array."""
    control = get_layout_control(ctrl)
    return cmds.paneLayout(control, q=True, childArray=True)


def destroy_window(*args):
    """If PlayView windows exist, destroy them."""
    for w in get_windows():
        if w.startswith(windowID):
            cmds.deleteUI(w)
    if cmds.window(helpID, exists=True):
        cmds.deleteUI(helpID)


def prefs_play_all(*args):
    """Check user prefs for viewport playback type."""
    if cmds.playbackOptions(q=True, v=True) == "all":
        return False
    else:
        return True


def init(*args):
    """Funtion to call to start the script."""
    if not prefs_play_all():
        play_button()
    else:
        if cmds.play(q=True, state=True) is True:
            play_button()
        else:
            global custom_viewport_tmp
            custom_viewport_tmp = ""

            sys.stdout.writelines(["Default: {}\n".format(custom_viewport)])

            if custom_viewport == "":
                destroy_window()
                draw_PlayView('PlayView')
            else:
                play_view(custom_viewport, default=True)