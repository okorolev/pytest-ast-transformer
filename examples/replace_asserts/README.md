About
-----
Replace `assert` to `my_assert`


Usage
-----

* Run 
    ```bash
    py.test -sv examples/replace_asserts/test_simple_assert.py
    ```
* Check output
    ```bash
    self = <tests.test_1.TestSimple object at 0x1058e72b0>
    
        def test_simple(self):
    >       assert 1 == 2, '1 is not 2'
    
    tests/test_1.py:24: 
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    
    test_result = False, msg = '1 is not 2'
    
        def my_assert(test_result, msg=''):
            print(f'my assert: {test_result} {msg}')
    >       assert test_result, msg
    E       AssertionError: 1 is not 2
    
    tests/transformer.py:8: AssertionError
    ```