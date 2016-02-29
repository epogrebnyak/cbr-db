import argparse
import logging
import logging.config
import os
import subprocess
import sys
import traceback


class ScriptError(Exception):
    """Custom exception class for convenient error handling in main()."""


def _configure_logging(verbose=True):
    """Configure logging (console only)."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=level)


def _parse_arguments(argv):
    """Builds ArgumentParser and returns the result of parse_args()."""
    parser = argparse.ArgumentParser(description='Batch execution of bankform commands')
    parser.add_argument('batch_name', help='Name of the batch to execute')
    parser.add_argument('form', help='CBR form number (e.g. 101)')
    parser.add_argument('dates', nargs='+', help='List of dates (YYYY or YYYY-MM-DD)')
    parser.add_argument('--regn', help='List of bank registration numbers')
    return parser.parse_args(argv[1:])


def _insert_arguments(command_template, args):
    """
    Inserts arguments into an command template.
    """
    result = []
    for template in command_template:
        if template == '{python}':
            result.append(sys.executable)
        elif template == '{script}':
            result.append('bankform.py')
        elif template == '{module}':
            result.append('cbr_db.bankform')
        elif template == '{form}':
            result.append(args.form)
        elif template == '{dates}':
            result.extend(args.dates)
        elif template == '{regn}':
            if args.regn:
                result.extend(('--regn', args.regn))
        elif template == '{report_format}':
            result.append('--xlsx')
        elif '{' in template or '}' in template:
            raise ScriptError('Unknown template variable: {!r}'.format(template))
        else:
            result.append(template)
    return result


_BATCHES = {
    'dummy': [
        ['{python}', '--version'],
        ['{python}', '-c', 'print("It works!")'],
    ],
    'simple': [
        ['{python}', '-m', '{module}', 'reset', 'database', 'raw'],
        ['{python}', '-m', '{module}', 'reset', 'database', 'final'],
        ['{python}', '-m', '{module}', 'download', '{form}', '{dates}'],
        ['{python}', '-m', '{module}', 'unpack', '{form}', '{dates}'],
        ['{python}', '-m', '{module}', 'make', 'csv', '{form}', '{dates}'],
        ['{python}', '-m', '{module}', 'import', 'csv', '{form}', '{dates}'],
        ['{python}', '-m', '{module}', 'make', 'dataset', '{form}', '{dates}'],
        ['{python}', '-m', '{module}', 'migrate', 'dataset', '{form}'],
        ['{python}', '-m', '{module}', 'make', 'balance'],
        ['{python}', '-m', '{module}', 'report', 'balance', '{report_format}'],
    ],
    'full': [
        ['{python}', '-m', '{module}', 'reset', 'database', 'raw'],
        ['{python}', '-m', '{module}', 'reset', 'database', 'final'],
        ['{python}', '-m', '{module}', 'update', '{form}', '{dates}'],
        ['{python}', '-m', '{module}', 'make', 'dataset', '{form}', '{dates}', '{regn}'],
        ['{python}', '-m', '{module}', 'migrate', 'dataset', '{form}'],
        ['{python}', '-m', '{module}', 'make', 'balance'],
        ['{python}', '-m', '{module}', 'report', 'balance', '{report_format}'],
    ],
}


def main(argv):
    args = _parse_arguments(argv)
    logger = logging.getLogger()
    try:
        _configure_logging()
        try:
            batch = _BATCHES[args.batch_name]
        except KeyError as ex:
            raise ScriptError('Unknown batch: {}'.format(ex.args[0]))
        # Insert template values, such as {form}
        batch = [_insert_arguments(x, args) for x in batch]
        # Execute batch
        cwd = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        env = dict(os.environ)
        env['CBR_DB_SETTINGS'] = 'settings'
        for command in batch:
            logger.info('Calling {!r}'.format(command))
            process = subprocess.Popen(command, cwd=cwd, env=env)
            returncode = process.wait()
            if returncode != 0:
                raise ScriptError('Child process returned {!r}'.format(returncode))
        return 0
    except ScriptError as ex:
        logger.error(str(ex))
    except Exception:
        logger.error('Unhandled exception: {}'.format(traceback.format_exc()))
        return 1
    except KeyboardInterrupt:
        logger.error('Ctrl+C is pressed')
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
