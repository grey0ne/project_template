'use server'
import type { Metadata } from "next";
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
import { ThemeProvider } from '@mui/material/styles';
import { Container, CssBaseline } from '@mui/material';
import { theme } from '@/app/theme';
import { Counters } from '@/next_utils/counters';
import { routing } from '@/next_utils/i18n/routing';
import { notFound } from 'next/navigation';
import { NextIntlClientProvider, hasLocale } from 'next-intl';
import { Locale } from "next-intl";
import { ErrorProvider } from '@/next_utils/notifications/NotificationsContext';
import { NotificationsContainer } from '@/next_utils/notifications/NotificationsContainer';

type LayoutParams = Promise<{ locale: Locale }>;


export async function generateMetadata(params: LayoutParams): Promise<Metadata> {
    return {
        title: 'Project Template',
    }
}


export default async function RootLayout({
    children,
    params
}: Readonly<{
    children: React.ReactNode;
    params: Promise<{locale: string}>;
}>) {

    const GTAG_ID = process.env.NEXT_PUBLIC_GTAG;
    const YM_ID = process.env.NEXT_PUBLIC_YM_ID;

    const {locale} = await params;
    if (!hasLocale(routing.locales, locale)) {
        notFound();
    }

    return (
        <html>
            <head>
                <Counters gtag_id={ GTAG_ID } ym_id={ YM_ID }/>
            </head>
            <body>
                <AppRouterCacheProvider options={{ enableCssLayer: true }}>
                    <ThemeProvider theme={theme}>
                        <NextIntlClientProvider>
                            <ErrorProvider>
                                <CssBaseline />
                                <Container maxWidth="xl" sx={{ mt: 4 }}>
                                    {children}
                                </Container>
                                <NotificationsContainer />
                            </ErrorProvider>
                        </NextIntlClientProvider>
                    </ThemeProvider>
                </AppRouterCacheProvider>
            </body>
        </html>
    );
}
