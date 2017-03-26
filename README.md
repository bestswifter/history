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

To call a specific line, you just need to enter the number(say you want to call the first command):

```bash
1
```

If there are too many results, you can pipe it to less or use tail -n:

`h xcodebuild | less`

and:

`h xcodebuild | tail -10`

It means you want to see 10 commands which are most frequently called.

As the picture below shows:

![](http://images.bestswifter.com/1479040989.png)

## How to install

Firstly, make sure you have installed `gsed`, which I think is a better version of `sed`, you can simplely use `brew install gnu-sed`.

Then the only thing you need to do is to add the script below to your .zshrc to make sure it's sourced everytime a new zsh process is started:

```bash
function h(){
    history | grep --color=always -i $1 | awk '{$1="";print $0}' | # 查找关键字，去掉左侧的是数字 \
    sort | uniq -c | sort -rn | awk '{$1="";print NR " " $0}' | # 先去重（需要排序）然后根据次数排序，再去掉次数 \
    tee ~/.histfile_color_result | gsed -r "s/\x1B\[([0-9]{1,3}((;[0-9]{1,3})*)?)?[m|K]//g" |  # 把带有颜色的结果写入临时文件，然后去除颜色 \
    awk '{$1="";print "function " NR "() {" $0 "; echo \": $(date +%s):0;"$0"\" >> ~/.histfile }"}' | # 构造 function，把 $0 写入到 histfile 中 \
    {while read line; do eval $line &>/dev/null; done}  # 调用 eval，让 function 生效
    cat ~/.histfile_color_result | sed '1!G;h;$!d' # 倒序输出，更容易看到第一条
}
```

Sometimes, when you execute command `which 1` in iTerm, you may get such an output which means that history doesn't work: `1: aliased to cd -`. This is usually because your system has defined an alias called `1` for you and override your new alias. To  avoid this, you can find out where these alias are: 

![](http://images.bestswifter.com/1489024112.png)

So just execute `vim ~/.oh-my-zsh/lib/directories.zsh` and add `# ` to those nine lines.

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

- [x] Limit maximum lines of output (Marked as completed because now you can use less/more)
- [x] Use shell command `history` instead of grep a file
- [ ] ~~Support serach directories you've visited~~(I think autojump is a better choice in most cases)
- [ ] Avoid output like `1. h xxx` because I think it is meaningless

For any suggestion or improvment or bug-fix, feel free to create an issue or make a pull request.
