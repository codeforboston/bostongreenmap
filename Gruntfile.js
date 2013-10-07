module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      production: {
        files: [{
          expand: true,
          flatten: false,
          cwd: 'bower_components/bootstrap/dist',
          dest: 'static/libs/bootstrap',
          src: ['**']
        }, {
          expand: true,
          flatten: true,
          cwd: 'bower_components',
          dest: 'static/libs/jquery',
          src: [
            'jquery/jquery.min.js', 'jquery/jquery.min.map', 
            'chosen/public/*.png', 'chosen/public/chosen.min.css', 'chosen/public/chosen.jquery.min.js',
            'purl/purl.js',
            'slidesjs3-bower/source/jquery.slides.min.js'
          ]
        },{
          expand: true,
          flatten: false,
          cwd: 'bower_components/leaflet/dist',
          dest: 'static/libs/leaflet',
          src: ['**']
        }, {
          expand: true,
          flatten: false,
          cwd: 'bower_components/handlebars',
          dest: 'static/libs',
          src: ['handlebars.js']
        }]
      }
    },
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task(s).
  grunt.registerTask('default', ['copy:production']);

};