#!/bin/sh

HOME=${HOME:=/home/$(whoami)}
LIB=$WHATSAPPBOT_PATH/lib

mkdir -p $WHATSAPPBOT_PATH/lib

# Download main bot class as single module (last -"*" word)
echo "==> WebWhatsapp-Wrapper installer v.0.0.1"
for i in $MAIN_MODULE $MODULE ; do
    echo "===> $i as ${i##*-}"
    git clone https://www.github.com/$i.git $(echo $LIB/${i##*-} )
done

# DOwnload plugins
# https://stackoverflow.com/questions/918886/how-do-i-split-a-string-on-a-delimiter-in-bash#918931
for i in $(echo $PLUGINS | tr ":" "\n" ) ; do
    echo "===> $i as ${i##*-}"
    git clone https://www.github.com/$i.git $(echo $LIB/${i##*-})
done

touch $WHATSAPPBOT_PATH/__init__.py
