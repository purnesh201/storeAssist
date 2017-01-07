export NODE_ENV=dev
cd /var/lib/jenkins/jobs/storeassist/workspace/web
npm install
bower install --allow-root
gulp build
