context('kernel')

Sys.setenv(
    PYTHONWARNINGS = 'ignore::DeprecationWarning',
    PYTHONPATH = paste(getwd(), Sys.getenv('PYTHONPATH'), sep = ':'))

suppressPackageStartupMessages(library(rPython))

python.load('get-tests.py', get.exception = TRUE)
test_descs <- python.get('test_descs')

for (desc in test_descs) {
    test_that(desc, {
        result <- python.call('run_test', desc)
        if (length(result$skipped) > 0L) {
            skip(paste(result$skipped, sep = '\n'))
        }
        if (length(result$failures) > 0L) {
            fail(paste(result$failures, sep = '\n'))
        }
        if (length(result$expected_failures) > 0L) {
            succeed(paste(result$expected_failures, sep = '\n'))
        }
        if (result$success)
            succeed('Success!')
        else
            fail('unknown reason')
    })
}
