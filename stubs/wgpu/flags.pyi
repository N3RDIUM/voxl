class BufferUsage:
    MAP_READ: int = 1
    MAP_WRITE: int = 2
    COPY_SRC: int = 4
    COPY_DST: int = 8
    INDEX: int = 16
    VERTEX: int = 32
    UNIFORM: int = 64
    STORAGE: int = 128
    INDIRECT: int = 256
    QUERY_RESOLVE: int = 512
