# frozen_string_literal: true

source "https://rubygems.org"

gemspec

gem "html-proofer", "~> 5.0", group: :test

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "jekyll-google_search_console_verification_file", "~> 1.1", :group => :jekyll_plugins
gem "wdm", "~> 0.2.0", :platforms => [:mingw, :x64_mingw, :mswin]
