"use client";

import * as Sentry from "@sentry/nextjs";
import NextError from "next/error";
import { useEffect } from "react";

export default function GlobalError({
    error,
}: {
    error: Error & { digest?: string };
}) {
    useEffect(() => {
        Sentry.captureException(error);
    }, [error]);

    return (
        <html>
            <body>
                {/* This is the default Next.js error component but it doesn't allow omitting the statusCode property yet. */}
                <NextError statusCode={undefined as any} />
            </body>
        </html>
    );
}