import argparse
import logging

def create_workflow_parser(subparsers):
    workflow_parser = subparsers.add_parser('workflow')
    workflow_subparsers = workflow_parser.add_subparsers(dest='workflow_command')

    create_parser = workflow_subparsers.add_parser('create')
    create_parser.add_argument('-o', '--output-file', type=str, help='Path to the output file', required=True)
    create_parser.add_argument('-l', '--log-level', choices=['info', 'debug', 'warning', 'error', 'critical'], default='info', help='Log level')

def create_trigger_parser(subparsers):
    trigger_parser = subparsers.add_parser('trigger')
    trigger_subparsers = trigger_parser.add_subparsers(dest='trigger_command')

    validate_parser = trigger_subparsers.add_parser('validate')
    validate_parser.add_argument('-l', '--log-level', choices=['info', 'debug', 'warning', 'error', 'critical'], default='info', help='Log level')

def create_parser():
    parser = argparse.ArgumentParser(prog='generate.py')
    subparsers = parser.add_subparsers(dest='command')

    create_workflow_parser(subparsers)
    create_trigger_parser(subparsers)

    return parser
