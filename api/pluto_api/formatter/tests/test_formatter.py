import pytest
from pluto_api.exceptions import AppError
from pluto_api.formatter import formatter

SIMPLE_TEMPLATE_TEST_CASE = {
    "input": """
!name1=Wade
!name2=Watts

Hello @name1 @name2
    """,
    "output": """
Hello Wade Watts
    """
}


SAMPLE_TEMPLATE_TEST_CASE = {
    "input": """
!name1=Wade
!name2=Watts
!avatar=Parzival
!salutation=Dear @name1 @name2 (aka @avatar)
101 IOI Plaza
!company=Innovative Online Industries
!product=OASIS Haptic Suit
!phone=1-800-SUPPORT
Columbus, OH 43123

@salutation,

Thank you for your interest in @{product}s. Unfortunately, we are not taking orders of the @product until early next year.

@name1, if you have any more questions about our products, email us at support@@ioi.com, tweet to @@ioi_support, or call us @@ @phone.

Thank you @avatar for being a valued member of the OASIS!!

Customer Support
@company
""",
    "output": """
101 IOI Plaza
Columbus, OH 43123

Dear Wade Watts (aka Parzival),

Thank you for your interest in OASIS Haptic Suits. Unfortunately, we are not taking orders of the OASIS Haptic Suit until early next year.

Wade, if you have any more questions about our products, email us at support@ioi.com, tweet to @ioi_support, or call us @ 1-800-SUPPORT.

Thank you Parzival for being a valued member of the OASIS!!

Customer Support
Innovative Online Industries
"""
}

BAD_VAR_DECLARATION = """
!!name1=Wade

Hello @name1
"""

BAD_INTERPOLATION = """
!name1=Wade

Hello @name1
Can you contact us @@@ 555-5555
"""

UNDEFINED_VARIABLE = """
!name1=Wade

Hello @name2
"""


def test_simple_template():
    """ Success Case: Test formatter with a simple template """

    output = formatter.template_formatter(SIMPLE_TEMPLATE_TEST_CASE["input"])
    assert output == SIMPLE_TEMPLATE_TEST_CASE["output"]


def test_sample_template():
    """ Success Case: Test formatter with a more detailed template """

    output = formatter.template_formatter(SAMPLE_TEMPLATE_TEST_CASE["input"])
    assert output == SAMPLE_TEMPLATE_TEST_CASE["output"]


def test_bad_variable_declaration():
    """ Fail Case: Test formatter with bad variable declaration """

    with pytest.raises(AppError):
        formatter.template_formatter(BAD_VAR_DECLARATION)


def test_bad_interpolation():
    """ Fail Case: Test formatter with properly escaped @ """

    with pytest.raises(AppError):
        formatter.template_formatter(BAD_INTERPOLATION)


def test_undefined_variable():
    """ Fail Case: Test formatter with undefined variable """

    with pytest.raises(AppError):
        formatter.template_formatter(UNDEFINED_VARIABLE)
