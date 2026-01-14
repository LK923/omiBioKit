from omibio.utils.chunked import chunked


class TestChunked:
    def test_general(self):
        s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chunks = list(chunked(s, chunk_size=2))
        assert chunks[0] == "AB"
        assert chunks[1] == "CD"
        assert chunks[3] == "GH"
        assert chunks[-1] == "YZ"
