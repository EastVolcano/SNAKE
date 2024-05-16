import math
import numpy as np
from scipy.spatial.transform import Rotation as R


a = 6378137
b = 6356752.3142
f = (a - b) / a


def wgs84ToNED(lat, lon, h, lat0=24.8976763, lon0=160.123456, h0=0):
    """
    :param lat: 当前lla
    :param lon: 当前lla
    :param h: 当前lla
    :param lat0: 原点lla
    :param lon0: 原点lla
    :param h0: 原点lla
    :return: N,E,D
    """
    x, y, z = wgs84ToEcef(lat, lon, h)
    North, East, Down = ecefToNed(x, y, z, lat0, lon0, h0)
    return North, East, Down


def ned_to_wgs84(ned_vec, lat0=24.8976763, lon0=160.123456, h0=0):
    """
    :param ned_vec: NED
    :param lat0: 原点lla
    :param lon0: 原点lla
    :param h0: 原点lla
    :return: lla
    """
    x, y, z = enu_to_ecef(ned_vec[1], ned_vec[0], -ned_vec[2], lat0, lon0, h0)
    lat, lon, alt = ecef_to_geodetic(x, y, z)
    return lon, lat, alt


def wgs84ToEcef(lat, lon, h):
    e_sq = f * (2 - f)
    lamb = math.radians(lat)
    phi = math.radians(lon)
    s = math.sin(lamb)
    N = a / math.sqrt(1 - e_sq * s * s)

    sin_lambda = math.sin(lamb)
    cos_lambda = math.cos(lamb)
    sin_phi = math.sin(phi)
    cos_phi = math.cos(phi)

    x = (h + N) * cos_lambda * cos_phi
    y = (h + N) * cos_lambda * sin_phi
    z = (h + (1 - e_sq) * N) * sin_lambda

    return x, y, z


def ecefToNed(x, y, z, lat, lng, height):
    """
    :param x: ecef
    :param y: ecef
    :param z: ecef
    :param lat: NED原点
    :param lng: NED原点
    :param height: NED原点
    :return: NED
    """
    e_sq = f * (2 - f)
    lamb = math.radians(lat)
    phi = math.radians(lng)
    s = math.sin(lamb)
    N = a / math.sqrt(1 - e_sq * s * s)
    sin_lambda = math.sin(lamb)
    cos_lambda = math.cos(lamb)
    sin_phi = math.sin(phi)
    cos_phi = math.cos(phi)

    x0 = (height + N) * cos_lambda * cos_phi
    y0 = (height + N) * cos_lambda * sin_phi
    z0 = (height + (1 - e_sq) * N) * sin_lambda

    xd = x - x0
    yd = y - y0
    zd = z - z0

    t = -cos_phi * xd - sin_phi * yd

    East = -sin_phi * xd + cos_phi * yd
    North = t * sin_lambda + cos_lambda * zd
    Up = cos_lambda * cos_phi * xd + cos_lambda * sin_phi * yd + sin_lambda * zd

    return North, East, -Up


def enu_to_ecef(xEast, yNorth, zUp, lat0, lon0, h0):
    e_sq = f * (2 - f)
    pi = 3.14159265359
    lamb = math.radians(lat0)
    phi = math.radians(lon0)
    s = math.sin(lamb)
    N = a / math.sqrt(1 - e_sq * s * s)

    sin_lambda = math.sin(lamb)
    cos_lambda = math.cos(lamb)
    sin_phi = math.sin(phi)
    cos_phi = math.cos(phi)

    x0 = (h0 + N) * cos_lambda * cos_phi
    y0 = (h0 + N) * cos_lambda * sin_phi
    z0 = (h0 + (1 - e_sq) * N) * sin_lambda

    t = cos_lambda * zUp - sin_lambda * yNorth

    zd = sin_lambda * zUp + cos_lambda * yNorth
    xd = cos_phi * t - sin_phi * xEast
    yd = sin_phi * t + cos_phi * xEast

    x = xd + x0
    y = yd + y0
    z = zd + z0

    return x, y, z


def ecef_to_geodetic(x, y, z):
    e_sq = f * (2 - f)
    pi = 3.14159265359
    # Convert from ECEF cartesian coordinates to
    # latitude, longitude and height.  WGS-84
    x2 = x ** 2
    y2 = y ** 2
    z2 = z ** 2

    a = 6378137.0000  # earth radius in meters
    b = 6356752.3142  # earth semiminor in meters
    e = math.sqrt(1 - (b / a) ** 2)
    b2 = b * b
    e2 = e ** 2
    ep = e * (a / b)
    r = math.sqrt(x2 + y2)
    r2 = r * r
    E2 = a ** 2 - b ** 2
    F = 54 * b2 * z2
    G = r2 + (1 - e2) * z2 - e2 * E2
    c = (e2 * e2 * F * r2) / (G * G * G)
    s = (1 + c + math.sqrt(c * c + 2 * c)) ** (1 / 3)
    P = F / (3 * (s + 1 / s + 1) ** 2 * G * G)
    Q = math.sqrt(1 + 2 * e2 * e2 * P)
    ro = -(P * e2 * r) / (1 + Q) + math.sqrt(
        (a * a / 2) * (1 + 1 / Q) - (P * (1 - e2) * z2) / (Q * (1 + Q)) - P * r2 / 2)
    tmp = (r - e2 * ro) ** 2
    U = math.sqrt(tmp + z2)
    V = math.sqrt(tmp + (1 - e2) * z2)
    zo = (b2 * z) / (a * V)

    height = U * (1 - b2 / (a * V))

    lat = math.atan((z + ep * ep * zo) / r)

    temp = math.atan(y / x)
    if x >= 0:
        long = temp
    elif (x < 0) & (y >= 0):
        long = pi + temp
    else:
        long = temp - pi

    lat0 = lat / (pi / 180)
    lon0 = long / (pi / 180)
    h0 = height

    return lat0, lon0, h0


def euler2vector(roll=0, pitch=0, yaw=0):
    """
    :param roll: euler deg
    :param pitch: euler deg
    :param yaw: euler deg
    :return: the orientation vector (x,y,z) of object (numpy array)
    """
    phi = np.deg2rad(roll)
    theta = np.deg2rad(pitch)
    psi = np.deg2rad(yaw)

    vector = np.zeros(3)
    vector[0] = np.cos(theta) * np.cos(psi)
    vector[1] = np.cos(theta) * np.sin(psi)
    vector[2] = - np.sin(theta)

    return vector


def angle_2vec(vec1, vec2):
    """计算两个矢量的夹角"""
    # vec1= np.array([x, y, z])
    # vec2 = np.array([x1, y1, z1])

    # 分别计算两个向量的模：
    l_1 = np.sqrt(vec1.dot(vec1))
    l_2 = np.sqrt(vec2.dot(vec2))

    # 计算两个向量的点积
    dian=vec1.dot(vec2)

    # 计算夹角的cos值：
    cos_=dian/(l_1*l_2)

    # 求得夹角（弧度制）：
    angle_rad = np.arccos(cos_)

    # 弧度转角度
    return np.rad2deg(angle_rad)


# def ned_to_body(delta_pitch, delta_yaw, roll, pitch, yaw):
#     # 定义旋转矩阵
#     r_yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
#                       [np.sin(yaw), np.cos(yaw), 0],
#                       [0, 0, 1]])
#
#     r_pitch = np.array([[np.cos(pitch), 0, -np.sin(pitch)],
#                         [0, 1, 0],
#                         [np.sin(pitch), 0, np.cos(pitch)]])
#
#     r_roll = np.array([[1, 0, 0],
#                        [0, np.cos(roll), np.sin(roll)],
#                        [0, -np.sin(roll), np.cos(roll)]])
#
#     r = np.dot(np.dot(r_roll, r_pitch), r_yaw)
#
#     body_pos = np.dot(r, [np.cos(delta_pitch) * np.cos(delta_yaw),
#                           np.cos(delta_pitch) * np.sin(delta_yaw),
#                           np.sin(delta_pitch)])
#
#     delta_pitch_body = math.atan2(body_pos[2], math.sqrt(body_pos[0] ** 2 + body_pos[1] ** 2))
#     delta_yaw_body = math.atan2(body_pos[1], body_pos[0])
#
#     # 将角度转换为度数
#     delta_pitch_deg = math.degrees(delta_pitch_body)
#     delta_yaw_deg = math.degrees(delta_yaw_body)
#
#     return delta_pitch_deg, delta_yaw_deg


def vector_angle(vec1, vec2):
    dot = vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]
    crossX = vec1[1] * vec2[2] - vec1[2] * vec2[1]
    crossY = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    crossZ = vec1[0] * vec2[1] - vec1[1] * vec2[0]
    norm = np.sqrt(crossX * crossX + crossY * crossY + crossZ * crossZ)
    return (np.arctan2(norm, dot) / np.pi) * 180


def ned_to_body(vec, yaw, pitch, roll):
    """
    :param vec: 矢量在导航系下的表示
    :param yaw: 偏航角 角度
    :param pitch: 俯仰角 角度
    :param roll: 滚转角 角度
    :return: 矢量在机体系下的表示
    """
    # 地面系与机体系，依次绕y,z,x轴旋转，依次旋转偏航角，俯仰角，滚转角
    # r = R.from_euler('yzx', [yaw, pitch, roll], degrees=True)
    # R_ear2body = r.as_matrix()
    #
    # vec_body = np.matmul(R_ear2body.T, vec)

    r = R.from_euler('ZYX', [yaw, pitch, roll], degrees=True).inv()
    R_earth2body = r.as_matrix()
    vec_body = np.matmul(R_earth2body, vec)

    return vec_body


def euler2quat(roll=0, pitch=0, yaw=0):
	"""
	:param roll: 滚转角 rad
	:param picth: 俯仰角 rad
	:param yaw: 偏航角 rad
	:return: 四元数
	"""
	phi = roll
	theta = pitch
	psi = yaw
	q = np.ones(4)
	q[3] = np.cos(phi / 2) * np.cos(theta / 2) * np.cos(psi / 2) + np.sin(phi / 2) * np.sin(theta / 2) * np.sin(psi / 2)
	q[0] = np.sin(phi / 2) * np.cos(theta / 2) * np.cos(psi / 2) - np.cos(phi / 2) * np.sin(theta / 2) * np.sin(psi / 2)
	q[1] = np.cos(phi / 2) * np.sin(theta / 2) * np.cos(psi / 2) + np.sin(phi / 2) * np.cos(theta / 2) * np.sin(psi / 2)
	q[2] = np.cos(phi / 2) * np.cos(theta / 2) * np.sin(psi / 2) - np.sin(phi / 2) * np.sin(theta / 2) * np.cos(psi / 2)
	return q


