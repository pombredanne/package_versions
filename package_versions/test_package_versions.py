
from pytest import raises
from .package_versions import parse_dependency, VersionRange, VersionFormatError, VersionRangeMismatch


#todo: check that selection order doesn't matter
#todo: test some adjecent values 1.0 / 1.1 etc


def test_range_equality():
	range1 = VersionRange.raw(min=(1, 3), max=(2, 0), min_inclusive=True, max_inclusive=False)
	range2 = VersionRange.raw(min=(1, 3), max=(2, 0), min_inclusive=True, max_inclusive=False)
	assert range1 == range2
	range3 = VersionRange.raw(min=(1, 3), max=(2, 0), min_inclusive=False, max_inclusive=False)
	range4 = VersionRange.raw(min=(1, 3), max=(2, 1), min_inclusive=True, max_inclusive=False)
	range11 = VersionRange.raw(min=(3, 1), max=(2, 0), min_inclusive=True, max_inclusive=False)
	assert not range1 == range3
	assert not range1 == range4
	assert not range1 == range11
	range5 = VersionRange.raw(min=None, min_inclusive=True)
	range6 = VersionRange.raw(min=None, min_inclusive=False)
	range7 = VersionRange.raw(max=None, max_inclusive=True)
	range8 = VersionRange.raw(max=None, max_inclusive=False)
	assert range5 == range6
	assert range7 == range8
	range9 = VersionRange.raw(min=None, max=None)
	range10 = VersionRange.raw(min=None, max=None)
	assert range9 == range10


def test_range_raw_checks():
	with raises(AssertionError):
		VersionRange.raw(min=(1, 3, 5))
	with raises(AssertionError):
		VersionRange.raw(max=(1, 3, 5))
	with raises(AssertionError):
		VersionRange.raw(min='1.3')
	with raises(AssertionError):
		VersionRange.raw(min='1.3')
	with raises(AssertionError):
		VersionRange.raw(min_inclusive=12)
	with raises(AssertionError):
		VersionRange.raw(max_inclusive=12)


def test_range_checks():
	with raises(VersionRangeMismatch):
		VersionRange('<=2.2').add_selection('>2.3', conflict='error')
	with raises(VersionRangeMismatch):
		VersionRange('>2.3,<=2.2')
	with raises(VersionRangeMismatch):
		VersionRange('<=2.2,>2.3')
	with raises(VersionRangeMismatch):
		VersionRange('==2.*,<=1.9')
	#todo


def test_range_noconflict():
	vr = VersionRange('>4.2,<5')
	vr.add_selection('==4.3', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 3), max=(4, 3), min_inclusive=True, max_inclusive=True)
	vr = VersionRange('>4.2,<5')
	vr.add_selection('==4.*', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 2), max=(5, 0), min_inclusive=False, max_inclusive=False)
	vr = VersionRange('>4.0,<5')
	vr.add_selection('<4.5', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 0), max=(4, 5), min_inclusive=False, max_inclusive=False)
	vr = VersionRange('>4.0,<5')
	vr.add_selection('>=4.5', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 5), max=(5 ,0), min_inclusive=True, max_inclusive=False)
	vr = VersionRange('>4.0,<5')
	vr.add_selections('>4.2,<4.8', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 2), max=(4, 8), min_inclusive=True, max_inclusive=True)
	vr = VersionRange('>4.0,<5')
	vr.add_selections('>=4.2,<=4.8', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 2), max=(4, 8), min_inclusive=True, max_inclusive=True)
	vr = VersionRange('>4.0,<5')
	vr.add_selections('>4.5,<5.5', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 5), max=(5, 0), min_inclusive=False, max_inclusive=False)
	vr = VersionRange('>4.0,<5')
	vr.add_selections('>=2.5,<=4.8', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 0), max=(4, 8), min_inclusive=False, max_inclusive=True)
	vr = VersionRange('>4.0,<5')
	vr.add_selections('>3.15,<=5.0', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 3), max=(4, 3), min_inclusive=True, max_inclusive=True)


def test_range_conflict_resolution():
	vr = VersionRange('>2.3')
	vr.add_selection('<=2.2', conflict='silent')
	print('&&&', vr)
	assert vr == VersionRange.raw(min=(2, 3), max=None, min_inclusive=False)
	vr = VersionRange('<=2.2')
	vr.add_selection('>2.3', conflict='silent')
	assert vr == VersionRange.raw(min=(2, 3), max=None, min_inclusive=False)
	vr = VersionRange('>=2.3')
	vr.add_selection('<2.2', conflict='silent')
	assert vr == VersionRange.raw(min=(2, 3), max=None, min_inclusive=True)
	vr = VersionRange('<2.2')
	vr.add_selection('>=2.3', conflict='silent')
	assert vr == VersionRange.raw(min=(2, 3), max=None, min_inclusive=True)
	vr = VersionRange('>4.0,<5')
	vr.add_selection('<3.0', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 0), max=(5, 0), min_inclusive=False, max_inclusive=False)
	vr = VersionRange('>4.0,<5')
	vr.add_selection('>=5.0', conflict='silent')
	assert vr == VersionRange.raw(min=(5, 0), max=None, min_inclusive=True)
	vr = VersionRange('>=4.0,<=5')
	vr.add_selection('<=3.0', conflict='silent')
	assert vr == VersionRange.raw(min=(4, 0), max=(5, 0), min_inclusive=False, max_inclusive=False)
	vr = VersionRange('>=4.0,<=5')
	vr.add_selection('>5.0', conflict='silent')
	assert vr == VersionRange.raw(min=(5, 0), max=None, min_inclusive=False)


def test_intersection():
	pass
	#VersionRange('>=4.0,<=6.0') & VersionRange('>=3.0,<=5')
	#todo


def test_make_range():
	""" Note: single equality like =1.7 isn't officially supported, but don't break it without reason. """
	assert VersionRange('==*') == VersionRange('=*') == VersionRange.raw(min=None, max=None)
	assert VersionRange('==1.*') == VersionRange('=1.*') == VersionRange.raw(min=(1, 0), max=(2, 0), min_inclusive=True, max_inclusive=False)
	assert VersionRange('==2.7') == VersionRange('=2.7') == VersionRange.raw(min=(2, 7), max=(2, 7), min_inclusive=True, max_inclusive=True)
	assert VersionRange('>1.0') == VersionRange.raw(min=(1, 0), min_inclusive=False)
	assert VersionRange('>1.') == VersionRange('>1') == VersionRange.raw(min=(2, 0), min_inclusive=True)
	assert VersionRange('<1.') == VersionRange('<1') == VersionRange.raw(max=(1, 0), max_inclusive=False)
	assert VersionRange('>=1.') == VersionRange('>=1') == VersionRange.raw(min=(1, 0), min_inclusive=True)
	assert VersionRange('<=1.') == VersionRange('<=1') == VersionRange.raw(max=(2, 0), max_inclusive=False)
	assert VersionRange('>=3.4') == VersionRange.raw(min=(3, 4), min_inclusive=True)
	assert VersionRange('<9.0') == VersionRange.raw(max=(9, 0), max_inclusive=False)
	assert VersionRange('<=3.4') == VersionRange.raw(max=(3, 4), max_inclusive=True)
	assert VersionRange('==0.0') == VersionRange('==.0')
	assert VersionRange('==0.') == VersionRange('==.')
	assert VersionRange.raw(min=(2, 2), max=(2, 3), min_inclusive=True, max_inclusive=False) == VersionRange('>=2.2,<2.3')
	assert VersionRange.raw(min=(1, 3), max=(2, 0), min_inclusive=True, max_inclusive=False) == VersionRange('>=1.3,<2.0')


def test_incorrect_version():
	with raises(VersionFormatError):
		VersionRange('hello world')
	with raises(VersionFormatError):
		VersionRange('>=1.0.0')
	with raises(VersionFormatError):
		VersionRange('<1.0.0')
	with raises(VersionFormatError):
		VersionRange('=1.0.0')
	with raises(VersionFormatError):
		VersionRange('package==1.0')
	with raises(VersionFormatError):
		VersionRange('<=')
	with raises(VersionFormatError):
		VersionRange('9=')


def test_range_repr():
	for repr in ('>=1.3,<2.0', '==1.7', '==*'):
		assert str(VersionRange(repr)) == repr
	assert str(VersionRange('=37.0')) == '==37.0'
	assert str(VersionRange('==2.*,<2.5')) == '>=2.0,<2.5'
	assert str(VersionRange('<=1.4,>=1.4')) == '==1.4'
	assert str(VersionRange('==1.*')) == '>=1.0,<2.0'
	assert str(VersionRange('>=2.2,<2.3')) == '==2.2'
	assert str(VersionRange('>2.2,<=2.3')) == '==2.3'
	assert str(VersionRange('>2.2,<2.4')) == '==2.3'
	assert str(VersionRange('<3.0,>1.0')) == '>1.0,<3.0'
	#todo


def test_parse_dependency():
	assert parse_dependency('>=1.0') == ('', VersionRange('>=1.0'))
	assert parse_dependency('package==*') == ('package', VersionRange('==*'))


def test_comments():
	package1, range1=parse_dependency('package>=1.0#,<2.0')
	assert range1 == VersionRange('>=1.0')
	package2, range2=parse_dependency('package>=1. # hello world')
	assert package2 == 'package'
	assert range2 == VersionRange('>=1')
	with raises(VersionFormatError):
		parse_dependency('#package>=1.0')

