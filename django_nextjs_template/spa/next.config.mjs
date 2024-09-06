/** @type {import('next').NextConfig} */

import { withSentryConfig } from "@sentry/nextjs";

const nextConfig = {
    experimental: {
        instrumentationHook: true
    },
};

const sentryWebpackPluginOptions = {
    // Additional config options for the Sentry webpack plugin. Keep in mind that
    // the following options are set automatically, and overriding them is not
    // recommended:
    //   release, url, configFile, stripPrefix, urlPrefix, include, ignore
  
    org: process.env.SENTRY_ORG,
    project: process.env.SENTRY_PROJECT,
  
    // An auth token is required for uploading source maps.
    authToken: process.env.SENTRY_AUTH_TOKEN,
  
    silent: true, // Suppresses all logs
    hideSourceMaps: false,
    disableLogger: true
  
    // For all available options, see:
    // https://github.com/getsentry/sentry-webpack-plugin#options.
};

export default withSentryConfig(nextConfig, sentryWebpackPluginOptions);