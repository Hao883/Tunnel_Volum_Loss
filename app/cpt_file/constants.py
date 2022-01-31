"""Copyright (c) 2022 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from viktor import Color
from viktor.parametrization import OptionListElement
from viktor.views import MapLegend


DEFAULT_MIN_LAYER_THICKNESS = 200

ADDITIONAL_COLUMNS = ['corrected_depth', 'fs', 'u2', 'inclination', 'inclination_n_s', 'inclination_e_w']

DEFAULT_SOIL_NAMES = [
    OptionListElement('Grind, zwak siltig, los'),
    OptionListElement('Grind, zwak siltig, matig'),
    OptionListElement('Grind, zwak siltig, vast'),
    OptionListElement('Grind, sterk siltig, los'),
    OptionListElement('Grind, sterk siltig, matig'),
    OptionListElement('Grind, sterk siltig, vast'),
    OptionListElement('Zand, schoon, los'),
    OptionListElement('Zand, schoon, matig'),
    OptionListElement('Zand, schoon, vast'),
    OptionListElement('Zand, zwak siltig, kleiïg'),
    OptionListElement('Zand, sterk siltig, kleiïg'),
    OptionListElement('Leem, zwak zandig, slap'),
    OptionListElement('Leem, zwak zandig, matig'),
    OptionListElement('Leem, zwak zandig, vast'),
    OptionListElement('Leem, sterk zandig'),
    OptionListElement('Klei, schoon, slap'),
    OptionListElement('Klei, schoon, matig'),
    OptionListElement('Klei, schoon, vast'),
    OptionListElement('Klei, zwak zandig, slap'),
    OptionListElement('Klei, zwak zandig, matig'),
    OptionListElement('Klei, zwak zandig, vast'),
    OptionListElement('Klei, sterk zandig'),
    OptionListElement('Klei, organisch, slap'),
    OptionListElement('Klei, organisch, matig'),
    OptionListElement('Veen, niet voorbelast, slap'),
    OptionListElement('Veen, matig voorbelast, matig'),
]

CPT_LEGEND = MapLegend([
    (Color.viktor_black(), "CPT"),
])
