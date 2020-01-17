# sample_convex_combinations

> Samples from convex combination space.

In theory this module "only" provides a bit of math.
In practice, it's a useful piece of abstraction.

This module provides a function that pickes a convex combination of a
desired dimension (= number of items), uniformly distributed among all
convex combinations. It is possible supply your own RNG, or a
hand-picked point from a hypercube (uniform distribution in the
hypercube guarantees uniform distribution in "convex
combination"-space).

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [Contribute](#contribute)

## Install

Just `pip install sample_convex_combinations`. (As soon as I have uploaded it to PyPI.)

Or just copy `sample_convex_combinations/_impl.py` into your project as `sample_convex_combinations.py`.

There are no dependencies outside stdlib.

## Usage

Let's say you want to interpolate between three things, and wish the sum of the weights to be 1:

```
>>> import sample_convex_combinations
>>> sample_convex_combinations.sample(3)
[0.6847422669970515, 0.6847422669970515, 0.6847422669970515]  # FIXME
```

Or maybe you want the sum of the weights to be between 0 and 1:

```
>>> sample_convex_combinations.sample(3, span_origin=True)
[0.49931160565103394, 0.49931160565103394, 0.49931160565103394]  # FIXME
```

The default `random.random` is not enough for your needs?  Sure thing!
You can substitute your own RNG, for example from `secrets`:

```
>>> import secrets
>>> sample_convex_combinations.sample(3, rng=secrets.randbits(64) / (2 ** 64))
[0.49931160565103394, 0.49931160565103394, 0.49931160565103394]  # FIXME
```

Isn't that nice? :D

### Full documentation

FIXME

## TODOs

* Implement
* Document
* Do WeirdStuff™ with it
* Advertise

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/sample_convex_combinations/issues/new) or submit PRs.
