# History

History is a zsh script which internally uses python to handle data. 

With this script, you can easily find any command you've executed and call it again.

Your command history is stored **permanently**, you will not lose them even restaring your computer.

## How to use

Use command `h` followed by key word you want to search, for example, you don't remember how to execute `xcodebuild`

```bash
h xcodebuild
```

Then you will get all commands contains 'grep', each line begins with a number.

To call a specific line, you just need to enter the number(for eaxmple `1`):

```bash
21
```

If there are too many results, you can pipe it to less or use tail -n:

`h xcodebuild | less`

and:

`h xcodebuild | tail -10`

It means you want to see 10 commands which are most frequently called.

As the picture below shows:

![](http://images.bestswifter.com/1479040989.png)

## How to install

The only thing you need to do is to add the script below to your .zshrc to make sure it's sourced everytime a new zsh process is started:

```bash
function h(){
    history | grep --color=always $1 | awk '{$1="";print $0}' |\
    sort | uniq -c | sort -rn | awk '{$1="";print NR " " $0}' |\
    tee ~/.histfile_color_result | sed -r "s/\x1B\[([0-9]{1,3}((;[0-9]{1,3})*)?)?[m|K]//g" |\
    awk '{$1="";print "function " NR "() {" $0 "; echo \": $(date +%s):0;"$0"\" >> ~/.histfile }"}' |\
    {while read line; do eval $line &>/dev/null; done}
    cat ~/.histfile_color_result | sed '1!G;h;$!d'
}
```

## Feature

Compared to Ctrl-R, you can

1. Use regex to search command history
2. The result is sorted by frequence, which means the command will be more likely to be seen if is called more frequently
3. You can pipe it to more/less/tail/head
 
## Caution

Since you will use `grep` underhood, please escape your pattern. For example, to search a command comtains `-a`, you hava to use:

```bash
h "\-a"
```

I haven't test other environment so there is **no guarentee** that this command works as expected in other environments.

I recommand you to use iTerm3 + zsh

## TO-DO

1. Limit maximum lines of output
2. Use shell command `history` instead of grep a file
3. Support serach directories you've visited

For any suggestion or improvent or bug-fix, feel free to create an issue or make a pull request.
