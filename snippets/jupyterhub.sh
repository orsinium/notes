# add user into jupyter hub

useradd -G www-data -p "some_very_very_long_and_difficult_password" "$1" --home=/home/"$1"/ --shell=/bin/bash
mkdir -p /home/"$1"/jupyter
chown -R "$1":"$1" /home/"$1"/
chmod -R 770 /home/"$1"/jupyter

mkdir -p /home/"$1"/.local/share/jupyter
mkdir -p /home/"$1"/.jupyter/nbconfig

rm -r /home/"$1"/.local/share/jupyter
cp -r /root/.local/share/jupyter /home/"$1"/.local/share/

# cp /root/.jupyter/jupyter_notebook_config.py /home/"$1"/.jupyter/jupyter_notebook_config.py
cp /root/.jupyter/jupyter_notebook_config.json /home/"$1"/.jupyter/jupyter_notebook_config.json
sed -i -e 's/root/home\/$1/g' /home/"$1"/.jupyter/jupyter_notebook_config.json

echo '{"load_extensions": {"config/config_menu/main": true}}' > /home/"$1"/.jupyter/nbconfig/notebook.json
