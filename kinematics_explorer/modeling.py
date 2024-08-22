#!/usr/bin/python3
from typing import Optional, Sequence
from pathlib import Path
import argparse
import sys

from toolkit.argparse_tools import actions, parents

def feria_subparser() -> argparse.ArgumentParser:
    """Parent parser for FERIA command line inputs."""
    # FERIA steps
    feria_steps = []

    # Get default template
    template_file = pathlib.Path(__file__).resolve().parent / 'feria_template.in'

    # Parser
    phelp = 'Model kinematics with FERIA models'
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--template', action=actions.CheckFile,
                        default=template_file,
                        help='FERIA input template file')
    parser.add_argument('')
    parser.set_defaults(steps=feria_steps)

    return parser, phelp

def model_lines(args: Optional[Sequence] = None):
    """
    """
    # Check args
    if args is None:
        args = sys.argv[1:]

    # Command line options
    args_parents = [
        parents.logger('debug_modeling.log'),
    ]
    subpars = {
        'feria': feria_subparser(),
        }
    parser = argparse.ArgumentParser(
        description='Model line emission',
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=args_parents,
        conflict_handler='resolve',
    )
    parser.add_argument('--outdir', action=actions.MakePath,
                        default=Path('./modeling'),
                        help='Output directory for the models')
    parser.add_argument('config', action=actions.CheckFile,
                        help='Model configuration file')

    # Subparsers
    subparsers = parser.add_subparsers(title='Models',
                                       description='valid models',
                                       help='model names')
    for name, (parent, phelp) in subpars.items():
        subparser = subparsers.add_parser(name, parents=[parent], help=phelp)

    # Evaluate
    args = parser.parse_args(args)
    for step in args.steps:
        step(args)

if __name__ == '__main__':
    model_lines(sys.argv[1:])
