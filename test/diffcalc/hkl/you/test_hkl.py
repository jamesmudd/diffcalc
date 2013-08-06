###
# Copyright 2008-2011 Diamond Light Source Ltd.
# This file is part of Diffcalc.
#
# Diffcalc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Diffcalc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Diffcalc.  If not, see <http://www.gnu.org/licenses/>.
###


from diffcalc.util import DiffcalcException
from mock import Mock, call
from nose.tools import assert_raises  # @UnresolvedImport
from nose.tools import raises, eq_  # @UnresolvedImport
import diffcalc.util
from diffcalc.conf import settings
diffcalc.util.DEBUG = True


class TestYouHklCommands:

    def setUp(self):
        settings.configure(hardware=Mock(), geometry=Mock(), engine_name='you')
        settings.GEOMETRY.fixed_constraints = {}
        
        from diffcalc.hkl.you import hkl
        reload(hkl)
        
        self.hkl = hkl
        self.hkl._hklcalc = Mock()
        self.hkl._hklcalc.constraints.report_constraints_lines.return_value = ['report1', 'report2']

#    def test__str__(self):
#        self.hkl._hklcalc.__str__.return_value = 'abc'
#        eq_(self.hkl.__str__(), 'abc')

    def test_con_with_1_constraint(self):
        self.hkl.con('cona')
        self.hkl._hklcalc.constraints.constrain.assert_called_with('cona')

    def test_con_with_1_constraint_with_value(self):
        self.hkl.con('cona', 123)
        self.hkl._hklcalc.constraints.constrain.assert_called_with('cona')
        self.hkl._hklcalc.constraints.set_constraint.assert_called_with('cona', 123)

    def test_con_with_3_constraints(self):
        self.hkl.con('cona', 'conb', 'conc')
        self.hkl._hklcalc.constraints.clear_constraints.assert_called()
        calls = [call('cona'), call('conb'), call('conc')]
        self.hkl._hklcalc.constraints.constrain.assert_has_calls(calls)

    def test_con_with_3_constraints_first_val(self):
        self.hkl.con('cona', 1, 'conb', 'conc')
        self.hkl._hklcalc.constraints.clear_constraints.assert_called()
        calls = [call('cona'), call('conb'), call('conc')]
        self.hkl._hklcalc.constraints.constrain.assert_has_calls(calls)
        self.hkl._hklcalc.constraints.set_constraint.assert_called_with('cona', 1)

    def test_con_with_3_constraints_second_val(self):
        self.hkl.con('cona', 'conb', 2, 'conc')
        self.hkl._hklcalc.constraints.clear_constraints.assert_called()
        calls = [call('cona'), call('conb'), call('conc')]
        self.hkl._hklcalc.constraints.constrain.assert_has_calls(calls)
        self.hkl._hklcalc.constraints.set_constraint.assert_called_with('conb', 2)
        
    def test_con_with_3_constraints_third_val(self):
        self.hkl.con('cona', 'conb', 'conc', 3)
        self.hkl._hklcalc.constraints.clear_constraints.assert_called()
        calls = [call('cona'), call('conb'), call('conc')]
        self.hkl._hklcalc.constraints.constrain.assert_has_calls(calls)
        self.hkl._hklcalc.constraints.set_constraint.assert_called_with('conc', 3)
        
    def test_con_with_3_constraints_all_vals(self):
        self.hkl.con('cona', 1, 'conb', 2, 'conc', 3)
        self.hkl._hklcalc.constraints.clear_constraints.assert_called()
        calls = [call('cona'), call('conb'), call('conc')]
        self.hkl._hklcalc.constraints.constrain.assert_has_calls(calls)
        calls = [call('cona', 1), call('conb', 2), call('conc', 3)]
        self.hkl._hklcalc.constraints.set_constraint.assert_has_calls(calls)

        
    def test_con_messages_and_help_visually(self):
        self.hkl.con()
        print "**"
        print self.hkl.con.__doc__
        
    def test_con_message_display_whenn_selecting_an_unimplmented_mode(self):
        self.hkl._hklcalc.constraints.is_fully_constrained.return_value = True
        self.hkl._hklcalc.constraints.is_current_mode_implemented.return_value = False
        self.hkl.con('phi', 'chi', 'eta')
