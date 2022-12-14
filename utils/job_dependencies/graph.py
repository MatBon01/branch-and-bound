from collections import defaultdict

from typing_extensions import TypeAlias

Job: TypeAlias = int
Schedule: TypeAlias = list[Job]

JobGraph: TypeAlias = dict[Job, list[Job]]  # the edges of the job dependencies


node_types = [
    "onnx",
    "muse",
    "emboss",
    "emboss",
    "blur",
    "emboss",
    "vii",
    "blur",
    "wave",
    "blur",
    "blur",
    "emboss",
    "onnx",
    "onnx",
    "blur",
    "wave",
    "wave",
    "wave",
    "emboss",
    "onnx",
    "emboss",
    "onnx",
    "vii",
    "blur",
    "night",
    "muse",
    "emboss",
    "onnx",
    "wave",
    "emboss",
    "muse",
]

processing_times_by_type = {
    "vii": 20.1631,
    "blur": 6.0563,
    "night": 23.6028,
    "onnx": 3.2354,
    "emboss": 2.2412,
    "muse": 16.2930,
    "wave": 12.5938,
}

processing_times = [processing_times_by_type[node] for node in node_types]

due_times = [
    172,
    82,
    18,
    61,
    93,
    71,
    217,
    295,
    290,
    287,
    253,
    307,
    279,
    73,
    355,
    34,
    233,
    77,
    88,
    122,
    71,
    181,
    340,
    141,
    209,
    217,
    256,
    144,
    307,
    329,
    269,
]

links = [
    [0, 30],
    [1, 0],
    [2, 7],
    [3, 2],
    [4, 1],
    [5, 15],
    [6, 5],
    [7, 6],
    [8, 7],
    [9, 8],
    [10, 4],
    [11, 4],
    [12, 11],
    [13, 12],
    [14, 10],
    [15, 14],
    [16, 15],
    [17, 16],
    [18, 17],
    [19, 18],
    [20, 17],
    [21, 20],
    [22, 21],
    [23, 4],
    [24, 23],
    [25, 24],
    [26, 25],
    [27, 25],
    [28, 27],
    [29, 3],
    [29, 9],
    [29, 13],
    [29, 19],
    [29, 22],
    [29, 26],
    [29, 28],
]

N = len(node_types)


fixed_processing_times_by_type = {
    "vii": 21.0,
    "blur": 6.0,
    "night": 25.0,
    "onnx": 4.0,
    "emboss": 2.0,
    "muse": 17.0,
    "wave": 13.0,
}

fixed_processing_times = [fixed_processing_times_by_type[node] for node in node_types]
