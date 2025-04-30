import * as Sentry from "@sentry/nextjs";

const DSN = process.env.NEXT_PUBLIC_SENTRY_FRONTEND_DSN;
const VERSION = process.env.NEXT_PUBLIC_VERSION;

Sentry.init({
    dsn: DSN,
    release: VERSION,
    // Replay may only be enabled for the client-side
    tracesSampleRate: 0.1,

    integrations: [
        Sentry.replayIntegration(),
    ],
    replaysSessionSampleRate: 1.0,
    replaysOnErrorSampleRate: 1.0,

});

export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;