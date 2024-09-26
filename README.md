# [DEPRICATED] Clayton Roberts's Professional Website

**Note**: This website has been replaced with my [LinkedIn Profile](https://www.linkedin.com/in/claytonjroberts/).

This is my personal website with:

    +-------------{Heroku}---------------+
    |                                    |
    |  Python (Tornado) }--> Vue         |
    |  ^ Backend             ^ Frontend  |
    |                                    |
    +------------------------------------+

Access my website at <https://www.ClaytonJRoberts.com>

## Icon Credit

The [favicon](static/favicon.ico) was generated with a [favicon generator](https://favicon.io/favicon-generator/). Check out the [actual favicon](https://favicon.io/favicon-generator/?t=CJR&ff=Roboto&fs=60&fc=%23FBFBFB&b=rounded&bc=%23F05048).

# Debugging

To run the application, simply run the following:

```bash
# webpack
npm run-script build
# gunicorn --bind=0.0.0.0 --timeout 600 __main__:application
gunicorn -k tornado main:app
```
