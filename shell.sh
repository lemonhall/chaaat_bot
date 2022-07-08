# Press i first to enter edit mode
# In the first line type.
export PATH="~/opt/anaconda3/bin:$PATH"
# If you customized the installation location during installation, change ~/opt/anaconda3/bin to the bin folder in the customized installation directory

# The modified ~/.bash_profile file should look like this (where xxx is the username)
export PATH="~/opt/anaconda3/bin:$PATH"
# >>> conda initialize >>>
# !!! Contents within this block are managed by 'conda init' !!!
__conda_setup="$('/Users/lemonhall/opt/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
        eval "$__conda_setup"
else
        if [ -f "/Users/lemonhall/opt/anaconda3/etc/profile.d/conda.sh" ]; then
                . "/Users/lemonhall/opt/anaconda3/etc/profile.d/conda.sh"
        else
                export PATH="/Users/lemonhall/opt/anaconda3/bin:$PATH"
        fi
fi
unset __conda_setup
# <<< conda initialize <<<