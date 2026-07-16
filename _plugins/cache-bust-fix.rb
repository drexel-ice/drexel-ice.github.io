# Fixes the CSS fingerprint from the jekyll-cache-bust gem. The gem's
# bust_css_cache hashes assets/_sass/**/*, but this site's Sass sources
# live in _sass/ at the repo root (with the entry point in assets/css/),
# so the glob matched nothing and every deploy stamped main.css with
# MD5("") - the version never changed and browsers kept stale styles.
#
# Site plugins load after gem plugins, so registering this module last
# makes its bust_css_cache override the gem's.
require 'digest/md5'

module Jekyll
  module CacheBustFix
    SASS_GLOBS = ['_sass/**/*', 'assets/css/**/*.scss'].freeze

    def bust_css_cache(file_name)
      site = @context&.registers&.[](:site)
      base = site ? site.source : Dir.pwd
      content = SASS_GLOBS
                .flat_map { |glob| Dir[File.join(base, glob)].sort }
                .reject { |path| File.directory?(path) }
                .map { |path| File.read(path) }
                .join
      "#{file_name}?v=#{Digest::MD5.hexdigest(content)}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::CacheBustFix)
