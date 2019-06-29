from unittest import TestCase
from k2_util import mod_util
from tests.modules import test_module_a, test_module_b
import logging
import logger
import json

logger.configure_logging()

logger = logging.getLogger(__name__)


class ModUtilTests(TestCase):
    
    def test_create_mod(self):
        mod = mod_util.Mod(
            name='NAME',
            description='DESCRIPTION',
            file='FILE',
            members=[
                mod_util.ModMember(name='MEMBER_A'),
                mod_util.ModMember(name='MEMBER_B')
                ]
            )
        self.assertEqual(
            'NAME', 
            mod.name, 
            'Mod.name is incorrect')
        self.assertEqual(
            'DESCRIPTION', 
            mod.description, 
            'Mod.description is incorrect')
        self.assertEqual(
            'FILE', 
            mod.file, 
            'Mod.file is incorrect')
        self.assertEqual(
            2, 
            len(mod.members), 
            'Mod.members is incorrect')
        for member in mod.members:
            self.assertEqual(
                mod, 
                member.module,
                'Members of a module do not get their module parameter set')
    
    def test_mod__to_dict(self):
        mod = mod_util.Mod(
            name='NAME',
            description='DESCRIPTION',
            file='FILE',
            members=[
                mod_util.ModMember(name='MEMBER_A'),
                mod_util.ModMember(name='MEMBER_B')
                ]
            )
        dict = mod.to_dict()
        self.assertEqual(
            4, 
            len(dict), 
            'Mod.to_dict() does not contain the right number of entries')
        self.assertEqual(
            'NAME', 
            dict['name'], 
            'Mod.to_dict() name is incorrect')
        self.assertEqual(
            'DESCRIPTION', 
            dict['description'], 
            'Mod.to_dict() description is incorrect')
        self.assertEqual(
            'FILE', 
            dict['file'], 
            'Mod.to_dict() file is incorrect')
        self.assertEqual(
            2, 
            len(dict['members']), 
            'Mod.to_dict() members is incorrect')
    
    def test_create_mod_member(self):
        mod = mod_util.Mod(
            name='MOD_NAME',
            description='MOD_DESCRIPTION',
            file='MOD_FILE')
        mod_member = mod_util.ModMember(
            name='NAME',
            type='TYPE',
            description='DESCRIPTION',
            module=mod
            )
        
        self.assertEqual(
            'NAME', 
            mod_member.name, 
            'ModMember.name is incorrect')
        self.assertEqual(
            'DESCRIPTION', 
            mod_member.description, 
            'ModMember.description is incorrect')
        self.assertEqual(
            'TYPE', 
            mod_member.type, 
            'ModMember.type is incorrect')
        self.assertEqual(
            mod, 
            mod_member.module, 
            'ModMember.member is incorrect')
        self.assertEqual(
            1, 
            len(mod.members), 
            'Mod.members are not updated when a module member is created with a Mod')
    
    def test_mod_member__to_dict(self):
        mod = mod_util.Mod(
            name='MOD_NAME',
            description='MOD_DESCRIPTION',
            file='MOD_FILE')
        mod_member = mod_util.ModMember(
            name='NAME',
            type='TYPE',
            description='DESCRIPTION',
            module=mod
            )
        dict = mod_member.to_dict()
        self.assertEqual(
            3, 
            len(dict), 
            'ModMember.to_dict() does not contain the right number of entries')
        self.assertEqual(
            'NAME', 
            dict['name'], 
            'ModMember.to_dict() name is incorrect')
        self.assertEqual(
            'DESCRIPTION', 
            dict['description'], 
            'Mod.to_dict() description is incorrect')
        self.assertEqual(
            'TYPE', 
            dict['type'], 
            'ModMember.to_dict() type is incorrect')
    
    def test_scan_returns_details_of_module(self):
        mod = mod_util.scan(test_module_a)
        self.assertEqual(
            'tests.modules.test_module_a', 
            mod.name, 
            'Scanned module name is incorrect')
        self.assertEqual(
            'Test module A description', 
            mod.description.strip(), 
            'Scanned module description is incorrect')
        self.assertEqual(
            '/k2_util/tests/modules/test_module_a.py', 
            mod.file[-39:], 
            'Scanned module file is incorrect')
        self.assertEqual(
            'test_module_a', 
            mod.basename(), 
            'Scanned module basename is incorrect')
        self.assertEqual(
            'tests.modules', 
            mod.package_name(), 
            'Scanned module package_name is incorrect')

    def test_scan_returns_all_members_of_module(self):
        mod = mod_util.scan(test_module_a)
        self.assertEqual(
            13, 
            len(mod.members), 
            'Scanned module does not contain the right number of members')

    def test_scanned_members_have_correct_details(self):
        mod = mod_util.scan(test_module_a)
        member = mod.get_member(name='A_TEST_INTEGER')
        self.assertEqual(
            'A_TEST_INTEGER', 
            member.name,
            'Scanned member name is not correct')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.INTEGER, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'An integer value', 
            member.description,
            'Scanned member description is not correct')
        self.assertEqual(
            mod, 
            member.module,
            'Scanned member module is not correct')
        
        member = mod.get_member(name='A_TEST_DECIMAL')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.FLOAT, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'A float value', 
            member.description,
            'Scanned member description is not correct')
        
        member = mod.get_member(name='A_TEST_BOOLEAN')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.BOOLEAN, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'A boolean value', 
            member.description,
            'Scanned member description is not correct')
        
        member = mod.get_member(name='A_TEST_STRING')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.STRING, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'A string value', 
            member.description,
            'Scanned member description is not correct')
        
        member = mod.get_member(name='A_TEST_LIST')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.LIST, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'A list value', 
            member.description,
            'Scanned member description is not correct')
        
        member = mod.get_member(name='A_TEST_TUPLE')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.TUPLE, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'A tuple value', 
            member.description,
            'Scanned member description is not correct')
        
        member = mod.get_member(name='A_TEST_DICT')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.DICT, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'A dictionary value', 
            member.description,
            'Scanned member description is not correct')
        
        member = mod.get_member(name='a_test_function_a')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.FUNCTION, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'Test A Function A description', 
            member.description.strip(),
            'Scanned member description is not correct')
        
        member = mod.get_member(name='ATestClassA')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.CLASS, 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'Test A ATestClassA description', 
            member.description.strip(),
            'Scanned member description is not correct')
    
        member = mod.get_member(name='test_class_a')
        self.assertEqual(
            'tests.modules.test_module_a.ATestClassA', 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'An instance of tests.modules.test_module_a.ATestClassA.\n\n    Test A ATestClassA description', 
            member.description.strip(),
            'Scanned member description is not correct')
    
        member = mod.get_member(name='test_class_b')
        self.assertEqual(
            'tests.modules.test_module_a.ATestClassB', 
            member.type,
            'Scanned member type is not correct')
        self.assertEqual(
            'An instance of tests.modules.test_module_a.ATestClassB.\n\n    Test A ATestClassB description', 
            member.description.strip(),
            'Scanned member description is not correct')
        
    def test__member_to_member_type(self):
        self.assertEqual(
            mod_util.ModMember.MemberTypes.INTEGER, 
            mod_util._member_to_member_type(1), 
            'Failed to identify integers')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.FLOAT, 
            mod_util._member_to_member_type(1.0), 
            'Failed to identify floats')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.BOOLEAN, 
            mod_util._member_to_member_type(True), 
            'Failed to identify booleans')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.STRING, 
            mod_util._member_to_member_type(''), 
            'Failed to identify strings')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.LIST, 
            mod_util._member_to_member_type([]), 
            'Failed to identify lists')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.TUPLE, 
            mod_util._member_to_member_type(()), 
            'Failed to identify tuples')
        self.assertEqual(
            mod_util.ModMember.MemberTypes.DICT, 
            mod_util._member_to_member_type({}), 
            'Failed to identify dictionaries')
        def func():
            pass
        self.assertEqual(
            mod_util.ModMember.MemberTypes.FUNCTION, 
            mod_util._member_to_member_type(func), 
            'Failed to identify functions')
        class Cls(object):
            pass
        self.assertEqual(
            mod_util.ModMember.MemberTypes.CLASS, 
            mod_util._member_to_member_type(Cls), 
            'Failed to identify classes')
        
    def test__member_to_description(self):
        self.assertEqual(
            'A boolean value', 
            mod_util._member_to_description(True))
        self.assertEqual(
            'An integer value', 
            mod_util._member_to_description(1))
        self.assertEqual(
            'A float value', 
            mod_util._member_to_description(1.0))
        self.assertEqual(
            'A string value', 
            mod_util._member_to_description('string'))
        self.assertEqual(
            'A list value', 
            mod_util._member_to_description([]))
        self.assertEqual(
            'A tuple value', 
            mod_util._member_to_description(()))
        self.assertEqual(
            'A dictionary value', 
            mod_util._member_to_description({}))
        def func_a():
            '''This is a function'''
            pass
        self.assertEqual(
            'This is a function', 
            mod_util._member_to_description(func_a))
        def func_b():
            pass
        self.assertEqual(
            'An undocumented function', 
            mod_util._member_to_description(func_b))
        class Cls_A(object):
            '''This is a class'''
            pass
        self.assertEqual(
            'This is a class', 
            mod_util._member_to_description(Cls_A))
        class Cls_B(object):
            pass
        self.assertEqual(
            'An undocumented class', 
            mod_util._member_to_description(Cls_B))

    def test_module__find_members(self):
        mod = mod_util.scan(test_module_a)
        
        find = mod.find_members(name='A_TEST_INTEGER')
        self.assertEqual(
            1, 
            len(find))

        find = mod.find_members(type=mod_util.ModMember.MemberTypes.STRING)
        self.assertEqual(
            1, 
            len(find))
        self.assertEqual(
            'A_TEST_STRING', 
            find[0].name)

    def test_module__get_member(self):
        mod = mod_util.scan(test_module_a)
        
        member = mod.get_member(name='A_TEST_INTEGER')
        self.assertNotEqual(
            None, 
            member, 
            'Mod.get_member did not return a member')
        
        def fail_no_member():
            member = mod.get_member(name='XXX')
        self.assertRaises(mod_util.MemberNotFound, fail_no_member)

        def fail_member_not_unique():
            member = mod.get_member(type=mod_util.ModMember.MemberTypes.FUNCTION)
        self.assertRaises(mod_util.MemberNotUnique, fail_member_not_unique)

if __name__ == '__main__':
    unittest.main()

