'use server'
import type { Metadata } from "next";
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
import { ThemeProvider } from '@mui/material/styles';
import { Grid } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import theme from '@/app/theme';
import { Counters } from '@/next_utils/counters';
import { Locale } from 'next-intl';

type LayoutParams = Promise<{ locale: Locale }>;

export async function generateMetadata(): Promise<Metadata> {
    return {}
}

export default async function RootLayout({
    children,
    params
}: Readonly<{
    children: React.ReactNode;
    params: LayoutParams;
}>) {

    const GTAG_ID = process.env.NEXT_PUBLIC_GTAG;
    const YM_ID = process.env.NEXT_PUBLIC_YM_ID;

    return (
        <html>
            <head>
                <Counters gtag_id={ GTAG_ID } ym_id={ YM_ID }/>
            </head>
            <body>
                <AppRouterCacheProvider options={{ enableCssLayer: true }}>
                    <ThemeProvider theme={theme}>
                        <CssBaseline />
                        <Grid container alignItems='center' direction='column'>
                            {children}
                        </Grid>
                    </ThemeProvider>
                </AppRouterCacheProvider>
            </body>
        </html>
    );
}
