import { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig: NextConfig = { 
    allowedDevOrigins: [process.env.PROJECT_DOMAIN || '',]
};

const sentryWebpackPluginOptions = {
    // Additional config options for the Sentry webpack plugin. Keep in mind that
    // the following options are set automatically, and overriding them is not
    // recommended:
    //   release, url, configFile, stripPrefix, urlPrefix, include, ignore
  
    org: process.env.SENTRY_ORG,
    project: `${process.env.PROJECT_NAME}-frontend`,
  
    // An auth token is required for uploading source maps.
    authToken: process.env.SENTRY_RELEASE_TOKEN,
  
    silent: true, // Suppresses all logs
    autoInstrumentServerFunctions: false,
    hideSourceMaps: false,
    disableLogger: true
};

export default withSentryConfig(nextConfig, sentryWebpackPluginOptions);