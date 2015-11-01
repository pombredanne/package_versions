
from package_versions.settings import VERSION_MAX, VersionTooHigh


def str2intrest(txt, mx = VERSION_MAX):
	if txt.count('.') == 0:
		major, minor, rest = '0' + txt, 0, ''
	elif txt.count('.') == 1:
		(major, minor), rest = txt.split('.'), ''
	else:
		major, minor, rest = txt.split('.', maxsplit = 2)
	major, minor = int(major), int(minor)
	if not (major < mx - 1 and minor < mx - 1):
		raise VersionTooHigh('version too high (major={0:d}, minor={1:d}, limit={2:d})'.format(major, minor, mx))
	return mx * major + minor, rest


def intrest2str(nr, rest, mx = VERSION_MAX):
	major, minor, rest = nr // mx, nr % mx, '.{0:s}'.format(rest) if rest else ''
	if not major < mx - 1:
		raise VersionTooHigh('version too high (input//limit={0:d}//{1:d}={2:d})'.format(nr, mx, major))
	return '{0:d}.{1:d}'.format(major, minor) + rest


def int2str(nr, mx = VERSION_MAX):
	return intrest2str(nr, '', mx=mx)


def str2int(txt, mx = VERSION_MAX):
	return str2intrest(txt, mx=mx)[0]


def get_max_version(mx = VERSION_MAX):
	return mx * mx + mx

