import * as Sentry from "@sentry/nextjs";

const DSN = process.env.NEXT_PUBLIC_SENTRY_FRONTEND_DSN;

Sentry.init({
    dsn: DSN,
    // Replay may only be enabled for the client-side
    tracesSampleRate: 0.1,

    integrations: [
        Sentry.replayIntegration(),
    ],
    replaysSessionSampleRate: 1.0,
    replaysOnErrorSampleRate: 1.0,

});