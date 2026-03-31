_git_union()
{
    local cur prev words cword
    _init_completion || return

    local opts="-s --sort -v --verbose -q --quiet -h --help --version"
    case "${prev}" in
        *)
            ;;
    esac

    if [[ "${cur}" == -* ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
        return
    fi

    COMPREPLY=( $(compgen -d -- "${cur}") )
}

complete -F _git_union git-union
