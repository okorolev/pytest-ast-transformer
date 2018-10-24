func_source = """
    def test_func(): 
        assert 1==2, 'some_msg'
"""

cls_source = """
    class TestX: 
        def test_func(self): assert True, 'some_msg'
"""


class TestPlugin:

    def test_simple_transformer(self, testdir, load_plugin):
        testdir.makepyfile(func_source)

        result = testdir.runpytest()

        result.stdout.fnmatch_lines([
            "    def test_func():",
            ">       assert 1==2, 'some_msg'"
        ])
        result.stdout.fnmatch_lines([
            "    def my_assert(test_result, msg):",
            "        print(f'my assert: {test_result} {msg}')",
            ">       assert test_result, msg",
            "E       AssertionError: some_msg"
        ])
        result.stdout.fnmatch_lines(['my assert: False some_msg'])
        assert result.ret == 1

    def test_disable_transforms(self, testdir, load_plugin):
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--disable-transforms')

        result.stdout.fnmatch_lines([
            "    def test_func():",
            ">       assert 1==2, 'some_msg'"
        ])
        assert result.ret == 1

    def test_show_code(self, testdir, load_plugin):
        testdir.makepyfile(func_source)

        result = testdir.runpytest('--show-code')

        result.stdout.fnmatch_lines([
            "def test_func():",
            "    my_assert((1 == 2), 'some_msg')"
        ])
        result.stdout.fnmatch_lines(['my assert: False some_msg'])
        assert result.ret == 1
