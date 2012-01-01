============================================
A pseudo-code job advert and its discontents
============================================
---------------------------------------------------------------------
A cringe-worth and divisive recruitment technique :: recruitment, php
---------------------------------------------------------------------

Based on the success of a highly tongue-in-cheek ad for a project manager, we
recently experimented with a similar approach for finding developers: a job ad
written in PHP. Now I appreciate this is deeply lame, but the results of the
campaign were quite surprising - more of which in a minute. First, hold your
nose and parse the following:

.. sourcecode:: php

    <?php
    class TangentLabs extends HoxtonWebCompany implements 
        InnovativeWebsites, WorldBeatingApplications, IngeniousECommerce 
    {
        const vacancyForBrilliantDevelopers = true;
        public $benefits = array(
            'Smartest web agency in London',
            'Working on inventive web apps, using cutting-edge technology',
            'Super-friendly work environment, working within genuinely brilliant dev team',
        );
        public $drawbacks = null;
        public $sampleProjects = array(
            'http://www.borders.co.uk',
            'http://www.labour.co.uk',
            'http://www.sap.com/education'
        );
        public static function offerJob(Developer $you) {
            return (self::hasTheSkills($you) && self::hasWowFactor($you));
        }
        private static function hasTheSkills($developer) {    
            $desiredSkills = array('Object-oriented PHP 5', 'Advanced MySQL', 'Flex/AS3'); 
            return (
                count(array_intersect($developer->skills, $desiredSkills)) > 1 &&
                (int)$developer->loveForCoding > 1 << 30
            );
        }
        private static function hasWowFactor($developer) {
            return ($developer instanceof creativeThinker &&
                sizeof($developer->brain) > floatval(strpad('1', 100, '0')) &&
                property_exists($developer, 'hungerForNewTechnologies'));
        }
    }
    $you = new Developer;
    if (true === TangentLabs::offerJob($you)) {
        throw new Party();
    }

It's actually quite a fun challenge to write a decent job ad in PHP, conveying
both the requirements and writing PHP code that isn't hilariously convoluted.
I'd tried to do the same in Bash later on when we were hiring a sys-admin, but
gave up after 5 minutes.

As you would expect with such a self-consciously smug job advert like this,
torrents of abuse came tumbling down? Salutations along the lines of "You
pretentious Shoreditch wankers..." and so forth. However, what was a little
unexpected were emails along the lines of:

    Hi, I really like your job ad - the best I've seen for ages. I live in
    California though and don't actually want to apply for a job.

How strange?  Who can be bothered to type up a complimentary cover letter for a
job they don't even want to apply for - most genuine applicants can't be
bothered to get the spelling and grammar right in their opening salvos.

Another consequence is that most applicant's responses are also written in PHP
pseudocode, which become a bit tiresome after the twentieth implementation of
``Developer`` - we were asking for it though.

Strangely though, the clinching factor for several candidates was the following
comment, left at the end of the ad:

.. sourcecode:: php

    // If you have questions, just ask, and if you’re a recruitment consultant don’t even 
    // think about emailing – our board won’t let us use you, even though you may have our 
    // literal exact perfect candidate just waiting for an interview. Sorry.

There's nothing like the mutual hatred of recruitment consultants to bring
people together.
