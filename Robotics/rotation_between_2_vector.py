import numpy as np


def two_vect_to_rot(origin, goal):

    T_location = np.asarray(goal)
    T_location_norm = T_location.copy()
    T_location_norm = T_location_norm / np.linalg.norm(T_location_norm)
    # originVector是原始向量
    originVector = np.asarray(origin)
    # print(T_location_norm)
    # @ 是向量点乘

    sita = np.arccos(T_location_norm @ originVector)
    # n_vector = T_location_norm.cross(originVector)
    n_vector = np.cross(T_location_norm, originVector)

    n_vector = n_vector / np.linalg.norm(n_vector)

    n_vector_invert = np.asanyarray(
        (
            [0, -n_vector[2], n_vector[1]],
            [n_vector[2], 0, -n_vector[0]],
            [-n_vector[1], n_vector[0], 0],
        )
    )

    # print(sita)
    # print(n_vector_invert)

    I = np.asarray(([1, 0, 0], [0, 1, 0], [0, 0, 1]))
    # 核心公式：见上图
    R_w2c = (
        I
        + np.sin(sita) * n_vector_invert
        + n_vector_invert @ (n_vector_invert) * (1 - np.cos(sita))
    )

    return R_w2c


if __name__ == "__main__":
    origin = np.asarray([0, 0, 1])
    goal = np.asarray([1, 0, 0])
    ans = two_vect_to_rot(origin, goal)
    print(ans)
