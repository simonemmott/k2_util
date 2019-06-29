'''
Test module A description
'''

A_TEST_INTEGER = 1
A_TEST_DECIMAL = 1.234
A_TEST_BOOLEAN = True
A_TEST_STRING = 'This is a string'
A_TEST_LIST = [1,2,3]
A_TEST_TUPLE = ('a', 'b', 'c')
A_TEST_DICT = {
        'key1': 'value 1',
        'key2': 'value 2',
        'key3': 'value 3'
    }

def a_test_function_b(arg1, arg2, arg3, *args, **kwargs):
    '''
    Test A Function B description
    '''
    print('Running test function A')
    
class ATestClassA(object):
    '''
    Test A ATestClassA description
    '''
    
    def __init__(self, *args, **kw):
        pass
    
    def __str__(self):
        return '<ATestClassA>'
    
    a_test_field_integer = 1
    a_test_field_decimal = 1.234
    a_test_field_boolean = False
    a_test_field_string = 'This is a string'
    a_test_field_list = [1,2,3]
    a_test_tuple = ('a','b','c')
    a_test_dict = {
        'key1': 'value 1',
        'key2': 'value 2',
        'key3': 'value 3'
    }
    
    def a_test_method_a(self, arg1, arg2, arg3, *args, **kwargs):
        '''
        ATestClassA.a_test_method_a description
        '''
        pass
    
    def a_test_method_b(self, arg1, arg2, arg3, *args, **kwargs):
        '''
        ATestClassA.a_test_method_b description
        '''
        pass
    
    class ATestSubClassA(object):
        '''
        ATestClassA.ATestSubClassA description
        '''
        field1 = 1
        field2 = 2
        def __init__(self):
            pass
        def method_a(self):
            pass
        def method_b(self):
            pass
        
    class ATestSubClassB(object):
        '''
        ATestClassA.ATestSubClassA description
        '''
        field1 = 1
        field2 = 2
        def __init__(self):
            pass
        def method_a(self):
            pass
        def method_b(self):
            pass
        
        
class ATestClassB(object):
    '''
    Test A ATestClassB description
    '''
    
    def __init__(self, *args, **kw):
        pass
    
    def __str__(self):
        return '<ATestClassB>'
    
    b_test_field_integer = 1
    b_test_field_decimal = 1.234
    b_test_field_boolean = False
    b_test_field_string = 'This is a string'
    b_test_field_list = [1,2,3]
    b_test_tuple = ('a','b','c')
    b_test_dict = {
        'key1': 'value 1',
        'key2': 'value 2',
        'key3': 'value 3'
    }
    
    def b_test_method_a(self, arg1, arg2, arg3, *args, **kwargs):
        '''
        BTestClassB.b_test_method_a description
        '''
        pass
    
    def b_test_method_b(self, arg1, arg2, arg3, *args, **kwargs):
        '''
        BTestClassB.b_test_method_b description
        '''
        pass
    
    class BTestSubClassA(object):
        '''
        ATestClassB.BTestSubClassA description
        '''
        field1 = 1
        field2 = 2
        def __init__(self):
            pass
        def method_a(self):
            pass
        def method_b(self):
            pass
        
    class BTestSubClassB(object):
        '''
        ATestClassB.BTestSubClassB description
        '''
        field1 = 1
        field2 = 2
        def __init__(self):
            pass
        def method_a(self):
            pass
        def method_b(self):
            pass
        
def a_test_function_a(arg1:int, arg2:ATestClassA, arg3='XXX', *args, **kwargs):
    '''
    Test A Function A description
    '''
    print('Running test function A')
    
test_class_a = ATestClassA()

test_class_b = ATestClassB()    
    
    
