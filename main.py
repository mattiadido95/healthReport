"""
applehealthdata.py: Extract data from Apple Health App's export.xml.

Copyright (c) 2016 Nicholas J. Radcliffe
Licence: MIT
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import sys

from xml.etree import ElementTree
from collections import Counter, OrderedDict

__version__ = '1.0'

from splitDataSource import filter_csv

import plot as pl

FIELDS = OrderedDict((
    ('sourceName', 's'),
    ('sourceVersion', 's'),
    ('device', 's'),
    ('type', 's'),
    ('unit', 's'),
    ('creationDate', 'd'),
    ('startDate', 'd'),
    ('endDate', 'd'),
    ('value', 'n'),
))

PREFIX_RE = re.compile('^HK.*TypeIdentifier(.+)$')
ABBREVIATE = True
VERBOSE = True


def format_freqs(counter):
    """
    Format a counter object for display.
    """
    return '\n\t'.join('%s: %d' % (tag, counter[tag])
                       for tag in sorted(counter.keys()))


def format_value(value, datatype):
    """
    Format a value for a CSV file, escaping double quotes and backslashes.

    None maps to empty.

    datatype should be
        's' for string (escaped)
        'n' for number
        'd' for datetime
    """
    if value is None:
        return ''
    elif datatype == 's':  # string
        return '"%s"' % value.replace('\\', '\\\\').replace('"', '\\"')
    elif datatype in ('n', 'd'):  # number or date
        return value
    else:
        raise KeyError('Unexpected format value: %s' % datatype)


def abbreviate(s):
    """
    Abbreviate particularly verbose strings based on a regular expression
    """
    m = re.match(PREFIX_RE, s)
    return m.group(1) if ABBREVIATE and m else s


def encode(s):
    """
    Encode string for writing to file.
    In Python 2, this encodes as UTF-8, whereas in Python 3,
    it does nothing
    """
    return s.encode('UTF-8') if sys.version_info.major < 3 else s


class HealthDataExtractor(object):
    """
    Extract health data from Apple Health App's XML export, export.xml.

    Inputs:
        path:      Relative or absolute path to export.xml
        verbose:   Set to False for less verbose output

    Outputs:
        Writes a CSV file for each record type found, in the same
        directory as the input export.xml. Reports each file written
        unless verbose has been set to False.
    """

    def __init__(self, path, verbose=VERBOSE):
        self.in_path = path
        self.verbose = verbose
        self.directory = os.path.abspath(os.path.split(path)[0])
        with open('data/dataExport.xml') as f:
            self.report('Reading data from %s . . . ' % path, end='\n')
            self.data = ElementTree.parse(f)
            self.report('done')
        self.root = self.data._root
        self.nodes = list(self.root)
        self.n_nodes = len(self.nodes)
        self.abbreviate_types()
        self.collect_stats()

    def report(self, msg, end='\n'):
        if self.verbose:
            print(msg, end=end)
            sys.stdout.flush()

    def count_tags_and_fields(self):
        self.tags = Counter()
        self.fields = Counter()
        for record in self.nodes:
            self.tags[record.tag] += 1
            for k in record.keys():
                self.fields[k] += 1

    def count_record_types(self):
        self.record_types = Counter()
        for record in self.nodes:
            if record.tag == 'Record':
                self.record_types[record.attrib['type']] += 1

    def count_sourceName(self):
        self.sourceName = Counter()
        for record in self.nodes:
            if record.tag == 'Record':
                self.sourceName[record.attrib['sourceName']] += 1

    def collect_stats(self):
        self.count_record_types()
        self.count_tags_and_fields()
        self.count_sourceName()

    def open_for_writing(self):
        self.handles = {}
        self.paths = []
        output_dir = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        path = os.path.join(output_dir, 'export.csv')
        for kind in self.record_types:
            f = open(path, 'w')
            f.write(','.join(FIELDS) + '\n')
            self.handles[kind] = f
            self.report('Opening %s for writing' % path)

    def abbreviate_types(self):
        """
        Shorten types by removing common boilerplate text.
        """
        for node in self.nodes:
            if node.tag == 'Record':
                if 'type' in node.attrib:
                    node.attrib['type'] = abbreviate(node.attrib['type'])

    def write_records(self):
        for node in self.nodes:
            if node.tag == 'Record':
                attributes = node.attrib
                kind = attributes['type']
                values = [format_value(attributes.get(field), datatype)
                          for (field, datatype) in FIELDS.items()]
                line = encode(','.join(values) + '\n')
                self.handles[kind].write(line)

    def close_files(self):
        for (kind, f) in self.handles.items():
            f.close()
            self.report('Written %s data.' % abbreviate(kind))

    def extract(self):
        self.open_for_writing()
        self.write_records()
        self.close_files()

    def report_stats(self):
        with open("output/report.txt", "w") as report_file:
            report_file.write(f'Tags:\n\t{format_freqs(self.tags)}\n\n')
            report_file.write(f'Fields:\n\t{format_freqs(self.fields)}\n\n')
            report_file.write(f'Record types:\n\t{format_freqs(self.record_types)}\n\n')
            report_file.write(f'Source Names:\n\t{format_freqs(self.sourceName)}\n\n')

        print('\nTags:\n\t%s\n\n' % format_freqs(self.tags))
        print('Fields:\n\t%s\n\n' % format_freqs(self.fields))
        print('Record types:\n\t%s\n\n' % format_freqs(self.record_types))
        print('Source Names:\n\t%s\n\n' % format_freqs(self.sourceName))


if __name__ == '__main__':

    """
        To have plot about data, run the two following commented parts.
    """

    # data = HealthDataExtractor('/data/dataExport.xml')
    # data.report_stats()
    # data.extract()

    sources = [
        {'label': 'Apple Watch di Mattia', 'value': 496776},
        {'label': 'Livelli O₂', 'value': 8},
        {'label': 'Oral-B', 'value': 298},
        {'label': 'Salute', 'value': 7},
        {'label': 'Zepp Life', 'value': 174396},
        {'label': 'iPhone di Mattia (8)', 'value': 881848},
    ]

    record_types = [
        {'label': 'ActiveEnergyBurned', 'value': 264442},
        {'label': 'AppleExerciseTime', 'value': 4044},
        {'label': 'AppleStandHour', 'value': 5543},
        {'label': 'AppleStandTime', 'value': 13814},
        {'label': 'AppleWalkingSteadiness', 'value': 80},
        {'label': 'AudioExposureEvent', 'value': 3},
        {'label': 'BasalEnergyBurned', 'value': 68215},
        {'label': 'BodyFatPercentage', 'value': 247},
        {'label': 'BodyMass', 'value': 324},
        {'label': 'BodyMassIndex', 'value': 323},
        {'label': 'DistanceCycling', 'value': 4988},
        {'label': 'DistanceWalkingRunning', 'value': 38409},
        {'label': 'EnvironmentalAudioExposure', 'value': 8281},
        {'label': 'FlightsClimbed', 'value': 2609},
        {'label': 'HKDataTypeSleepDurationGoal', 'value': 1},
        {'label': 'HeadphoneAudioExposure', 'value': 3513},
        {'label': 'HeadphoneAudioExposureEvent', 'value': 4},
        {'label': 'HeartRate', 'value': 1040578},
        {'label': 'HeartRateRecoveryOneMinute', 'value': 10},
        {'label': 'HeartRateVariabilitySDNN', 'value': 2237},
        {'label': 'Height', 'value': 1},
        {'label': 'LeanBodyMass', 'value': 247},
        {'label': 'LowHeartRateEvent', 'value': 7},
        {'label': 'OxygenSaturation', 'value': 2983},
        {'label': 'RespiratoryRate', 'value': 4405},
        {'label': 'RestingHeartRate', 'value': 376},
        {'label': 'SexualActivity', 'value': 4},
        {'label': 'SixMinuteWalkTestDistance', 'value': 31},
        {'label': 'SleepAnalysis', 'value': 7411},
        {'label': 'StairAscentSpeed', 'value': 716},
        {'label': 'StairDescentSpeed', 'value': 857},
        {'label': 'StepCount', 'value': 45492},
        {'label': 'ToothbrushingEvent', 'value': 298},
        {'label': 'VO2Max', 'value': 58},
        {'label': 'WalkingAsymmetryPercentage', 'value': 3409},
        {'label': 'WalkingDoubleSupportPercentage', 'value': 6854},
        {'label': 'WalkingHeartRateAverage', 'value': 315},
        {'label': 'WalkingSpeed', 'value': 11102},
        {'label': 'WalkingStepLength', 'value': 11102},
    ]

    # input_file = "output/export.csv"
    # for source in sources:
    #     field1 = source['label']
    #     for record_type in record_types:
    #         field2 = record_type['label']
    #         print(field1, field2)
    #         output_file = filter_csv(input_file, field1, field2)

    pl.plot_csv_data('output/splitted/Apple Watch di Mattia_DistanceWalkingRunning.csv')
