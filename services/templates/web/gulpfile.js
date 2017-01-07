var gulp = require('gulp'),
    browserSync = require('browser-sync').create(),
    sass = require('gulp-sass'),
    preprocess = require('gulp-preprocess'),
    url = require('url'),
    proxy = require('proxy-middleware');
    handlebars = require('gulp-handlebars');
    wrap = require('gulp-wrap');
    declare = require('gulp-declare');
    concat = require('gulp-concat');

// Static server https: true
gulp.task('serve', ['sass'], function () {
  var proxyOptions = url.parse('http://localhost:5000/api');
  proxyOptions.route = '/api';
  browserSync.init({
    server: {
      baseDir: './',
      middleware: [proxy(proxyOptions)]
    }

  })
  gulp.watch('src/styles/**/*.scss', ['sass'])
  gulp.watch('*.html').on('change', browserSync.reload)
  gulp.watch('src/js/views/*.mustache').on('change', browserSync.reload)
})
// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function () {
  return gulp.src('./src/styles/main.scss')
    .pipe(sass().on('error', function (err) { console.error('Error!', err.message) }))
    .pipe(sass({includePaths: ['./src/styles']})).pipe(gulp.dest('dist/css'))
    .pipe(browserSync.stream());
})
gulp.task('scripts', function() {
  gulp.src(['src/js/app.js'])
    .pipe(preprocess({context: { production: true}}))
    .pipe(gulp.dest('src/js/app.js',{overwrite: true}))
});
gulp.task('fontmove', function(){
  gulp.src(['bower_components/bootstrap-sass-official/assets/fonts/**','bower_components/fontawesome/fonts/*'])
  .pipe(gulp.dest('dist/fonts'));
});
gulp.task('default', ['serve','templates'])
gulp.task('build', ['templates','fontmove','sass'])
gulp.task('templates', function(){
  gulp.src('src/js/views/*.hbs')
    .pipe(handlebars())
    .pipe(wrap('Handlebars.template(<%= contents %>)'))
    .pipe(declare({
      namespace: 'MyApp.templates',
      noRedeclare: true, // Avoid duplicate declarations
    }))
    .pipe(concat('templates.js'))
    .pipe(gulp.dest('build/js/'));
});
