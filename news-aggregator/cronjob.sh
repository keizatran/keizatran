# 00 22 * * *: excute at 22pm every day
cd /home/keiza/.repo/news-aggregator
git checkout main # excute on branch
python3 -u main_dynamic.py

git add log/publisher_scraping.log
git commit -m 'add log of new day'
git push