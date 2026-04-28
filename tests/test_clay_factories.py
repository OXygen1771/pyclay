"""Test clay structure factories."""

import pytest


def test_make_clay_string(validation_enabled_mode: None) -> None:
    """Test that make_clay_string() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_String
    from pyclay._clay.factories import make_clay_string

    s: Clay_String = make_clay_string("Test")
    assert s.length == 4
    assert not s.isStaticallyAllocated
    assert s.chars is not None

    from ctypes import string_at

    assert string_at(s.chars, s.length) == b"Test"


def test_make_clay_string_slice(validation_enabled_mode: None) -> None:
    """Test that make_clay_string_slice() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_StringSlice
    from pyclay._clay.factories import make_clay_string_slice

    s: Clay_StringSlice = make_clay_string_slice("Test")
    assert s.chars is not None
    assert (s.length, s.baseChars) == (4, s.chars)

    from ctypes import string_at

    assert string_at(s.chars, s.length) == b"Test"

    s2: Clay_StringSlice = make_clay_string_slice("Test", "Test 2")
    assert s2.length == 4
    assert s2.chars is not None
    assert s2.baseChars is not None
    assert s2.baseChars != s2.chars

    assert string_at(s2.chars, s2.length) == b"Test"
    assert string_at(s2.baseChars, len(b"Test 2")) == b"Test 2"


def test_make_clay_arena(validation_enabled_mode: None) -> None:
    """Test that make_clay_arena() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_Arena
    from pyclay._clay.factories import make_clay_arena

    with pytest.raises(ValueError, match=r"Arena capacity (size_t)*"):
        make_clay_arena(-1)

    cap: int = 64
    a: Clay_Arena = make_clay_arena(cap)
    assert (a.nextAllocation, a.capacity) == (0, cap)
    assert a.memory is not None

    from ctypes import string_at

    mem: bytes = string_at(a.memory, cap)
    assert len(mem) == cap

    # there should probably be a test for creating an arena with pre-allocated memory


def test_make_clay_dimensions(validation_enabled_mode: None) -> None:
    """Test that make_clay_dimensions() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_Dimensions
    from pyclay._clay.factories import make_clay_dimensions

    with pytest.raises(ValueError, match=r"Width*"):
        make_clay_dimensions(-1, 100)
    with pytest.raises(ValueError, match=r"Height*"):
        make_clay_dimensions(100, -1)

    width: int = 800
    height: int = 600
    d: Clay_Dimensions = make_clay_dimensions(width, height)
    assert (d.width, d.height) == (width, height)

    width2: float = 10e10
    height2: float = 10e11
    d2: Clay_Dimensions = make_clay_dimensions(width2, height2)
    eps: float = 5000  # float32 can't equal 10^10, let alone 10^11
    assert width2 - eps <= d2.width <= width2 + eps
    assert height2 - eps <= d2.height <= height2 + eps


def test_make_clay_vector2(validation_enabled_mode: None) -> None:
    """Test that make_clay_vector2() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_Vector2
    from pyclay._clay.factories import make_clay_vector2

    x: float = -3.5
    y: float = 0.1
    v: Clay_Vector2 = make_clay_vector2(x, y)
    eps: float = 0.00001
    assert x - eps <= v.x <= x + eps
    assert y - eps <= v.y <= y + eps


def test_make_clay_color(validation_enabled_mode: None) -> None:
    """Test that make_clay_color() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_Color
    from pyclay._clay.factories import make_clay_color

    c: Clay_Color = make_clay_color(1, 2, 3, 4)
    assert (c.r, c.g, c.b, c.a) == (1, 2, 3, 4)


def test_make_clay_bounding_box(validation_enabled_mode: None) -> None:
    """Test that make_clay_bounding_box() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_BoundingBox
    from pyclay._clay.factories import make_clay_bounding_box

    bb: Clay_BoundingBox = make_clay_bounding_box(0, 0, 100, 200)
    assert (bb.x, bb.y, bb.width, bb.height) == (0, 0, 100, 200)


def test_make_clay_element_id(validation_enabled_mode: None) -> None:
    """Test that make_clay_element_id() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_ElementId, Clay_String
    from pyclay._clay.factories import make_clay_element_id

    eid: Clay_ElementId = make_clay_element_id(0, 1, 2, "3")
    assert (eid.id, eid.offset, eid.baseId) == (0, 1, 2)

    from ctypes import string_at

    id_str: Clay_String = eid.stringId
    assert id_str.chars is not None
    assert string_at(id_str.chars, id_str.length) == b"3"


def test_clay_element_id_array_contextmanager(validation_enabled_mode: None) -> None:
    """Test that the clay_element_id_array() context manager works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_ElementId
    from pyclay._clay.factories import clay_element_id_array, make_clay_element_id

    ids: list[Clay_ElementId] = [
        make_clay_element_id(0, string_id="0"),
        make_clay_element_id(1, string_id="1"),
    ]

    with clay_element_id_array(ids) as arr:
        assert arr.capacity == len(ids)
        assert arr.length == len(ids)
        assert arr.internalArray is not None

        for i in range(arr.length):
            internal: Clay_ElementId = arr.internalArray[i]
            assert (
                internal.id,
                internal.offset,
                internal.baseId,
                bytes(internal.stringId),
            ) == (ids[i].id, ids[i].offset, ids[i].baseId, bytes(ids[i].stringId))

    # check cleanup
    assert not arr.internalArray
    with pytest.raises(ValueError, match=r"NULL*"):
        _ = arr.internalArray[0]

    with clay_element_id_array([]) as arr:
        assert arr.capacity == 0
        assert arr.length == 0
        assert not arr.internalArray


def test_make_clay_corner_radius(validation_enabled_mode: None) -> None:
    """Test that make_clay_corner_radius() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_CornerRadius
    from pyclay._clay.factories import make_clay_corner_radius

    cr: Clay_CornerRadius = make_clay_corner_radius(1, 2, 3, 4)
    assert (cr.topLeft, cr.topRight, cr.bottomLeft, cr.bottomRight) == (1, 2, 3, 4)


def test_make_clay_child_alignment(validation_enabled_mode: None) -> None:
    """Test that make_clay_child_alignment() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_ChildAlignment
    from pyclay._clay.factories import make_clay_child_alignment
    from pyclay.enums import LayoutAlignmentX, LayoutAlignmentY

    ca: Clay_ChildAlignment = make_clay_child_alignment()
    assert (ca.x, ca.y) == (LayoutAlignmentX.default(), LayoutAlignmentY.default())

    ca1: Clay_ChildAlignment = make_clay_child_alignment(0, 0)
    assert (ca1.x, ca1.y) == (LayoutAlignmentX(0), LayoutAlignmentY(0))


def test_make_clay_sizing_min_max(validation_enabled_mode: None) -> None:
    """Test that make_clay_sizing_min_max() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_SizingMinMax
    from pyclay._clay.factories import make_clay_sizing_min_max

    smm: Clay_SizingMinMax = make_clay_sizing_min_max()
    assert (smm.min, smm.max) == (0, float("inf"))

    smm1: Clay_SizingMinMax = make_clay_sizing_min_max(1, 2)
    assert (smm1.min, smm1.max) == (1, 2)


def test_make_clay_sizing_axis(validation_enabled_mode: None) -> None:
    """Test that make_clay_sizing_axis() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_SizingAxis, Clay_SizingMinMax
    from pyclay._clay.factories import make_clay_sizing_axis, make_clay_sizing_min_max
    from pyclay.enums import SizingType

    sa: Clay_SizingAxis = make_clay_sizing_axis()
    assert sa.type == SizingType.default()
    c_smm: Clay_SizingMinMax = sa.size.minMax
    smm: Clay_SizingMinMax = make_clay_sizing_min_max()
    assert (c_smm.min, c_smm.max) == (smm.min, smm.max)
    sa = make_clay_sizing_axis(0)
    assert sa.type == SizingType.default()

    sa_p: Clay_SizingAxis = make_clay_sizing_axis(SizingType.PERCENT)
    assert sa_p.type == SizingType.PERCENT
    assert sa_p.size.percent == 1
    sa_p = make_clay_sizing_axis(SizingType.PERCENT, percent=0.5)
    assert sa_p.type == SizingType.PERCENT
    eps: float = 0.00001
    assert 0.5 - eps <= sa_p.size.percent <= 0.5 + eps


def test_make_clay_sizing(validation_enabled_mode: None) -> None:
    """Test that make_clay_sizing() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_Sizing, Clay_SizingAxis
    from pyclay._clay.factories import (
        make_clay_sizing,
        make_clay_sizing_axis,
        make_clay_sizing_min_max,
    )
    from pyclay.enums import SizingType

    ax_w: Clay_SizingAxis = make_clay_sizing_axis()
    ax_h: Clay_SizingAxis = make_clay_sizing_axis(
        sizing_type=SizingType.GROW,
        min_max=make_clay_sizing_min_max(min_sizing=10),
    )
    s: Clay_Sizing = make_clay_sizing(width=ax_w, height=ax_h)
    w: Clay_SizingAxis = s.width
    h: Clay_SizingAxis = s.height
    assert (w.type, w.size.minMax.min, w.size.minMax.max) == (
        ax_w.type,
        ax_w.size.minMax.min,
        ax_w.size.minMax.max,
    )
    assert (h.type, h.size.minMax.min, h.size.minMax.max) == (
        ax_h.type,
        ax_h.size.minMax.min,
        ax_h.size.minMax.max,
    )


def test_make_clay_padding(validation_enabled_mode: None) -> None:
    """Test that make_clay_padding() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_Padding
    from pyclay._clay.factories import make_clay_padding

    p: Clay_Padding = make_clay_padding(1, 2, 3, 4)
    assert (p.left, p.right, p.top, p.bottom) == (1, 2, 3, 4)


def test_make_clay_layout_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_layout_config() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import (
        Clay_LayoutConfig,
        Clay_Padding,
    )
    from pyclay._clay.factories import (
        make_clay_child_alignment,
        make_clay_layout_config,
        make_clay_padding,
        make_clay_sizing,
        make_clay_sizing_axis,
    )
    from pyclay.enums import LayoutDirection

    lc: Clay_LayoutConfig = make_clay_layout_config(
        sizing=make_clay_sizing(
            width=make_clay_sizing_axis(),
            height=make_clay_sizing_axis(),
        ),
        padding=make_clay_padding(1, 2, 3, 4),
        child_alignment=make_clay_child_alignment(),
        child_gap=10,
    )
    assert lc.layoutDirection == LayoutDirection.default()
    p: Clay_Padding = lc.padding
    assert (p.left, p.right, p.top, p.bottom) == (1, 2, 3, 4)
    # other fields probably don't need testing?...

    lc = make_clay_layout_config(
        sizing=make_clay_sizing(
            width=make_clay_sizing_axis(),
            height=make_clay_sizing_axis(),
        ),
        padding=make_clay_padding(1, 2, 3, 4),
        child_alignment=make_clay_child_alignment(),
        child_gap=10,
        layout_direction=0,
    )
    assert lc.layoutDirection == LayoutDirection(0)


def test_make_clay_text_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_text_element_config() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_TextElementConfig
    from pyclay._clay.factories import make_clay_color, make_clay_text_element_config
    from pyclay.enums import TextAlignment, TextElementConfigWrapMode

    tc: Clay_TextElementConfig = make_clay_text_element_config(
        text_color=make_clay_color(1, 2, 3, 4),
        font_id=5,
        font_size=6,
        letter_spacing=7,
        line_height=8,
    )
    assert tc.wrapMode == TextElementConfigWrapMode.default()
    assert tc.textAlignment == TextAlignment.default()
    assert tc.userData is None

    tc = make_clay_text_element_config(
        text_color=make_clay_color(1, 2, 3, 4),
        font_id=5,
        font_size=6,
        letter_spacing=7,
        line_height=8,
        wrap_mode=0,
        text_alignment=1,
    )
    assert tc.wrapMode == TextElementConfigWrapMode(0)
    assert tc.textAlignment == TextAlignment(1)

    # test user_data
    from ctypes import c_void_p

    user_ptr = c_void_p(0xABCD)
    tc = make_clay_text_element_config(
        text_color=make_clay_color(1, 2, 3, 4),
        font_id=5,
        font_size=6,
        letter_spacing=7,
        line_height=8,
        user_data=user_ptr,
    )
    assert tc.userData is not None
    assert tc.userData == user_ptr.value


def test_make_clay_aspect_ratio_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_aspect_ratio_element_config() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_AspectRatioElementConfig
    from pyclay._clay.factories import make_clay_aspect_ratio_element_config

    ar: Clay_AspectRatioElementConfig = make_clay_aspect_ratio_element_config(1.5)
    eps: float = 0.00001
    assert 1.5 - eps <= ar.aspectRatio <= 1.5 + eps


def test_make_clay_image_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_image_element_config() works properly."""
    _v: None = validation_enabled_mode

    from ctypes import c_void_p

    from pyclay._clay._types import Clay_ImageElementConfig
    from pyclay._clay.factories import make_clay_image_element_config

    im_ptr: c_void_p = c_void_p(0xABCD)
    ic: Clay_ImageElementConfig = make_clay_image_element_config(im_ptr)
    assert ic.imageData is not None
    assert ic.imageData == im_ptr.value


def test_make_clay_floating_attach_points(validation_enabled_mode: None) -> None:
    """Test that make_clay_floating_attach_points() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_FloatingAttachPoints
    from pyclay._clay.factories import make_clay_floating_attach_points
    from pyclay.enums import FloatingAttachPointType

    fp: Clay_FloatingAttachPoints = make_clay_floating_attach_points()
    assert (fp.element, fp.parent) == (
        FloatingAttachPointType.default(),
        FloatingAttachPointType.default(),
    )

    fp = make_clay_floating_attach_points(0, 0)
    assert (fp.element, fp.parent) == (
        FloatingAttachPointType(0),
        FloatingAttachPointType(0),
    )


def test_make_clay_floating_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_floating_element_config() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import (
        Clay_FloatingAttachPoints,
        Clay_FloatingElementConfig,
    )
    from pyclay._clay.factories import (
        make_clay_dimensions,
        make_clay_floating_attach_points,
        make_clay_floating_element_config,
        make_clay_vector2,
    )
    from pyclay.enums import (
        FloatingAttachToElement,
        FloatingClipToElement,
        PointerCaptureMode,
    )

    fc: Clay_FloatingElementConfig = make_clay_floating_element_config(
        offset=make_clay_vector2(0, 1),
        expand=make_clay_dimensions(3, 4),
        z_index=5,
    )
    assert (fc.offset.x, fc.offset.y) == (0, 1)
    assert (fc.expand.width, fc.expand.height) == (3, 4)
    assert (fc.zIndex, fc.parentId) == (5, 0)
    assert (fc.pointerCaptureMode, fc.attachTo, fc.clipTo) == (
        PointerCaptureMode.default(),
        FloatingAttachToElement.default(),
        FloatingClipToElement.default(),
    )
    att_p: Clay_FloatingAttachPoints = make_clay_floating_attach_points()
    fc_att_p: Clay_FloatingAttachPoints = fc.attachPoints
    assert (fc_att_p.element, fc_att_p.parent) == (att_p.element, att_p.parent)

    fc = make_clay_floating_element_config(
        offset=make_clay_vector2(0, 1),
        expand=make_clay_dimensions(3, 4),
        z_index=5,
        pointer_captrue_mode=0,
        attach_to=0,
        clip_to=0,
    )
    assert (fc.pointerCaptureMode, fc.attachTo, fc.clipTo) == (
        PointerCaptureMode(0),
        FloatingAttachToElement(0),
        FloatingClipToElement(0),
    )

    fc = make_clay_floating_element_config(
        offset=make_clay_vector2(0, 1),
        expand=make_clay_dimensions(3, 4),
        z_index=5,
        attach_to=FloatingAttachToElement.ATTACH_TO_ELEMENT_WITH_ID,
        parent_id=6,
    )
    fc_att_p: Clay_FloatingAttachPoints = fc.attachPoints
    assert (fc_att_p.element, fc_att_p.parent) == (att_p.element, att_p.parent)
    assert (fc.parentId, fc.attachTo) == (
        6,
        FloatingAttachToElement.ATTACH_TO_ELEMENT_WITH_ID,
    )

    with pytest.raises(ValueError, match=r"parent*"):
        _fc = make_clay_floating_element_config(
            offset=make_clay_vector2(0, 1),
            expand=make_clay_dimensions(3, 4),
            z_index=5,
            attach_to=FloatingAttachToElement.ATTACH_TO_ELEMENT_WITH_ID,
        )


def test_make_clay_custom_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_custom_element_config() works properly."""
    _v: None = validation_enabled_mode

    from ctypes import c_void_p

    from pyclay._clay._types import Clay_CustomElementConfig
    from pyclay._clay.factories import make_clay_custom_element_config

    c_ptr: c_void_p = c_void_p(0xABCD)
    cc: Clay_CustomElementConfig = make_clay_custom_element_config(c_ptr)
    assert cc.customData is not None
    assert cc.customData == c_ptr.value


def test_make_clay_clip_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_clip_element_config() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_ClipElementConfig, Clay_Vector2
    from pyclay._clay.factories import make_clay_clip_element_config, make_clay_vector2

    cc: Clay_ClipElementConfig = make_clay_clip_element_config(
        horizontal=True,
        vertical=True,
        child_offset=make_clay_vector2(0, 1),
    )
    c_vec: Clay_Vector2 = cc.childOffset
    assert (cc.horizontal, cc.vertical, c_vec.x, c_vec.y) == (True, True, 0, 1)


def test_make_clay_border_width(validation_enabled_mode: None) -> None:
    """Test that make_clay_border_width() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import Clay_BorderWidth
    from pyclay._clay.factories import make_clay_border_width

    bw: Clay_BorderWidth = make_clay_border_width(0, 1, 2, 3, 4)
    assert (bw.left, bw.right, bw.top, bw.bottom, bw.betweenChildren) == (0, 1, 2, 3, 4)


def test_make_clay_border_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_border_element_config() works properly."""
    _v: None = validation_enabled_mode

    from pyclay._clay._types import (
        Clay_BorderElementConfig,
        Clay_BorderWidth,
        Clay_Color,
    )
    from pyclay._clay.factories import (
        make_clay_border_element_config,
        make_clay_border_width,
        make_clay_color,
    )

    bc: Clay_BorderElementConfig = make_clay_border_element_config(
        color=make_clay_color(0, 1, 2, 3),
        width=make_clay_border_width(4, 5, 6, 7, 8),
    )
    col: Clay_Color = bc.color
    width: Clay_BorderWidth = bc.width
    assert (col.r, col.g, col.b, col.a) == (0, 1, 2, 3)
    assert (
        width.left,
        width.right,
        width.top,
        width.bottom,
        width.betweenChildren,
    ) == (4, 5, 6, 7, 8)


def test_make_clay_transition_element_config(validation_enabled_mode: None) -> None:
    """Test that make_clay_transition_element_config() works properly."""
    _v: None = validation_enabled_mode

    from ctypes import CFUNCTYPE, c_uint32

    from pyclay._clay._types import (
        Clay_TransitionCallbackArguments,
        Clay_TransitionData,
        Clay_TransitionElementConfig,
        transitionHandlerFunction,
    )
    from pyclay._clay.factories import make_clay_transition_element_config
    from pyclay.enums import (
        ExitTransitionSiblingOrdering,
        TransitionEnterTriggerType,
        TransitionExitTriggerType,
        TransitionInteractionHandlingType,
        TransitionProperty,
        TransitionState,
    )

    def dummy_transition_args() -> Clay_TransitionCallbackArguments:
        args = Clay_TransitionCallbackArguments()
        args.transitionState = TransitionState.default()
        args.elapsedTime = 0.5
        args.duration = 1
        args.properties = TransitionProperty.NONE

        return args

    tc: Clay_TransitionElementConfig = make_clay_transition_element_config(duration=1)
    assert tc.duration == 1
    assert tc.handler is not None
    assert type(tc.handler) is transitionHandlerFunction
    assert callable(tc.handler)
    args: Clay_TransitionCallbackArguments = dummy_transition_args()
    res: bool = tc.handler(args)
    assert isinstance(res, bool)
    assert tc.properties == TransitionProperty.default()
    assert tc.interactionHandling == TransitionInteractionHandlingType.default()
    assert tc.enter is not None
    assert tc.exit is not None
    assert (tc.enter.trigger, tc.exit.trigger) == (
        TransitionEnterTriggerType.default(),
        TransitionExitTriggerType.default(),
    )
    set_state_type = CFUNCTYPE(Clay_TransitionData, Clay_TransitionData, c_uint32)
    assert (type(tc.enter.setInitialState), type(tc.exit.setFinalState)) == (
        set_state_type,
        set_state_type,
    )
    assert tc.exit.siblingOrdering == ExitTransitionSiblingOrdering(0)

    # dummy handler
    tc = make_clay_transition_element_config(
        duration=1,
        handler=lambda _args: True,
        properties=0,
        interaction_handling=0,
    )
    assert tc.properties == TransitionProperty(0)
    assert tc.interactionHandling == TransitionInteractionHandlingType(0)
    assert tc.handler is not None
    assert type(tc.handler) is transitionHandlerFunction
    assert callable(tc.handler)
    args: Clay_TransitionCallbackArguments = dummy_transition_args()
    res: bool = tc.handler(args)
    assert isinstance(res, bool)
    assert res is True


def test_make_clay_element_declaration(validation_enabled_mode: None) -> None:
    """Test that make_clay_element_declaration() works properly."""
    _v: None = validation_enabled_mode

    from ctypes import c_void_p

    from pyclay._clay._types import Clay_ElementDeclaration, Clay_Sizing
    from pyclay._clay.factories import (
        make_clay_child_alignment,
        make_clay_color,
        make_clay_element_declaration,
        make_clay_layout_config,
        make_clay_padding,
        make_clay_sizing,
        make_clay_sizing_axis,
        make_clay_sizing_min_max,
    )
    from pyclay.enums import SizingType

    el: Clay_ElementDeclaration = make_clay_element_declaration(
        layout=make_clay_layout_config(
            sizing=make_clay_sizing(
                width=make_clay_sizing_axis(
                    sizing_type=SizingType(0),
                    min_max=make_clay_sizing_min_max(1, 2),
                ),
                height=make_clay_sizing_axis(
                    sizing_type=SizingType.PERCENT,
                    percent=0.5,
                ),
            ),
            padding=make_clay_padding(3, 4, 5, 6),
            child_alignment=make_clay_child_alignment(0, 1),
            child_gap=3,
        ),
        background_color=make_clay_color(4, 5, 6, 7),
    )
    ls: Clay_Sizing = el.layout.sizing
    assert (ls.width.type, ls.width.size.minMax.min, ls.width.size.minMax.max) == (
        0,
        1,
        2,
    )
    assert (ls.height.type, ls.height.size.percent) == (SizingType.PERCENT, 0.5)

    user_ptr: c_void_p = c_void_p(0xABCD)
    el: Clay_ElementDeclaration = make_clay_element_declaration(
        layout=make_clay_layout_config(
            sizing=make_clay_sizing(
                width=make_clay_sizing_axis(
                    sizing_type=SizingType(0),
                    min_max=make_clay_sizing_min_max(1, 2),
                ),
                height=make_clay_sizing_axis(
                    sizing_type=SizingType.PERCENT,
                    percent=0.5,
                ),
            ),
            padding=make_clay_padding(3, 4, 5, 6),
            child_alignment=make_clay_child_alignment(0, 1),
            child_gap=3,
        ),
        background_color=make_clay_color(4, 5, 6, 7),
        user_data=user_ptr,
    )
    assert el.userData is not None
    assert el.userData == user_ptr.value
