project(
  'git-union',
  version: run_command('git', 'describe', '--tags', '--always', '--dirty',
                       check: false, capture: true).stdout().strip(),
  license: 'AGPL-3.0-or-later'
)

# Extract version components for use in configuration
version_str = meson.project_version()
version_parts = version_str.split('.')
major_version = version_parts.get(0, '0')
minor_version = version_parts.get(1, '0')
patch_version = version_parts.get(2, '0')

# Configure the main script with version substitution
configured_git_union = configure_file(
  input: 'git-union',
  output: 'git-union',
  configuration: {
    'PROJECT_VERSION': version_str
  },
  copy: false
)

# Install the configured script
install_data(configured_git_union,
  install_dir: get_option('prefix') / get_option('bindir'),
  rename: 'git-union'
)

# Install bash completion
install_data('git-union.bash',
  install_dir: get_option('prefix') / 'share' / 'bash-completion' / 'completions' / 'git-union'
)

# Install man page
install_data('git-union.1',
  install_dir: get_option('prefix') / 'share' / 'man' / 'man1'
)

# Install tests
install_data('tests/test_git_union.py',
  install_dir: get_option('prefix') / 'share' / 'git-union' / 'tests'
)

# Summary
summary({
  'Version': version_str,
  'Prefix': get_option('prefix'),
  'Bindir': get_option('prefix') / get_option('bindir'),
}, section: 'git-union', list_sep: '\n')
